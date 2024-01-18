import os
import re
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.helper.customExceptions import LoginFailedError

# Edge Import
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

desired_dpi = 2.0
options = webdriver.EdgeOptions()
options.add_argument(f"--force-device-scale-factor={desired_dpi}")
options.add_argument("--headless")
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)


def init_books(e_mail: str, passwd: str) -> tuple[bool, list] | tuple[bool, None]:
    logged_in = login_sap_press(e_mail=e_mail, passwd=passwd)

    if logged_in:
        success, book_list = get_book_list()
        cont = input("Continue: y/n? ")
        if cont.lower() == "y" or " ":
            return success, book_list if success else (False, None)

    return False, None


def login_sap_press(e_mail: str, passwd: str) -> bool:
    driver.get("https://www.sap-press.com/accounts/login/?next=/")

    try:
        driver.find_element(By.ID, "id_login-username").send_keys(e_mail)
        driver.find_element(By.ID, "id_login-password").send_keys(passwd)
        driver.find_element(By.XPATH, "//button[@name='login_submit']").click()
        print("\nLogging in...")

        # waits for the 'login failed' page to appear, if it doesn't, raises the TimeoutException and continues
        try:
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="login-input"]/div[1]')))
            raise LoginFailedError()
        except TimeoutException:
            print("\nLogged in successfully!")
            return True

    except LoginFailedError as e:
        print(e)
        driver.quit()
        return False

    except Exception:
        raise LoginFailedError


def get_book_list() -> tuple[bool, None] | tuple[bool, list]:
    driver.get("https://library.sap-press.com/library/")

    try:
        product_details = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "product-detail")))
    except NoSuchElementException:
        return False, None

    result_list = []

    for product_detail in product_details:
        title_element = product_detail.find_element(By.CLASS_NAME, "titel")
        title = title_element.text.strip()
        clean_name = re.sub(r"[^a-zA-Z0-9\s]", '', title)
        href = title_element.find_element(By.CSS_SELECTOR, "a.read-link").get_attribute('href')

        result_dict = {'title': clean_name, 'href': href}
        result_list.append(result_dict)
        print(f"Book: '{clean_name}' added to list.")

    return True, result_list


def get_book_pages(book_url, page_nr=1, max_attempts=3) -> tuple[bool, str] | tuple[bool, None]:
    output_directory = 'files/1.rawPictures'

    response = requests.get(book_url)
    if response.status_code == 200:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        print('\nNavigating to book...')
        driver.get(book_url)
    else:
        print(f"\nFailed to load the book page. Received status code: {response.status_code}")

    time.sleep(2)

    try:
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="lastReadPanel"]/a[2]'))).click()
    except TimeoutException:
        pass

    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="reader_nav"]/ul/li[3]/ul/li[4]/a'))).click()
    except TimeoutException:
        pass

    driver.set_window_size(1500, 1800)

    try:
        while True:
            element = WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div[4]/div[1]/div[1]/ul/li[8]/a[2]/span')))

            time.sleep(4)  # timer to wait for the full loading of the page (adjust based on internet quality)
            driver.save_screenshot(f'{output_directory}/{str(page_nr).zfill(2)}.png')
            print(f"Page: '{page_nr}' copied")
            page_nr += 1
            driver.execute_script("arguments[0].click();", element)

    except TimeoutException:
        print("\nReached the last page.")
        driver.quit()
        return True, output_directory

    except NoSuchElementException:
        if max_attempts > 0:
            print("\nElement not found. Retrying...")
            return get_book_pages(book_url=book_url, page_nr=page_nr, max_attempts=max_attempts - 1)
        else:
            print("\nMax attempts reached. Exiting.")
            driver.quit()
            return False, None

    except Exception as e:
        print(f"\nError: {e}")
        driver.quit()
        return False, None

import os
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.helper.customExceptions import LoginFailedError


def capture_book_pages(e_mail: str, passwd: str, book_url: str) -> tuple[bool, str] | tuple[bool, None]:

    directory = 'files/rawPictures'
    if not os.path.exists(directory):
        os.makedirs(directory)

    success, driver = login_sap_press(e_mail=e_mail, passwd=passwd)
    if success:
        success, output_folder = get_book_pages(driver=driver, book_url=book_url, output_directory=directory)
        return success, output_folder
    else:
        return success, None


def login_sap_press(e_mail: str, passwd: str) -> tuple[bool, WebDriver] | tuple[bool, None]:
    desired_dpi = 2.0
    options = webdriver.ChromeOptions()
    options.add_argument(f"--force-device-scale-factor={desired_dpi}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.sap-press.com/accounts/login/?next=/")

    try:
        driver.find_element(By.ID, "id_login-username").send_keys(e_mail)
        driver.find_element(By.ID, "id_login-password").send_keys(passwd)
        driver.find_element(By.XPATH, "//button[@name='login_submit']").click()
        print("Logging in...")

        # waits for the 'login failed' page to appear, if it doesn't, raises the TimeoutException and continues
        try:
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="login-input"]/div[1]')))
            raise LoginFailedError()
        except TimeoutException:
            print("Logged in successfully!")
            return True, driver

    except LoginFailedError as e:
        print(e)
        driver.quit()
        return False, None

    except Exception:
        raise LoginFailedError


def get_book_pages(driver, book_url, output_directory, page_nr=1, max_attempts=3) -> tuple[bool, str] | tuple[bool, None]:

    response = requests.get(book_url)
    if response.status_code == 200:
        print('Navigating to book...')
        driver.get(book_url)
    else:
        print(f"Failed to load the book page. Received status code: {response.status_code}")

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
            element = WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div[4]/div[1]/div[1]/ul/li[8]/a[2]/span')))

            # timer to wait for the full loading of the page
            time.sleep(5)
            driver.save_screenshot(f'{output_directory}/{str(page_nr).zfill(2)}.png')
            print(f"Page: '{page_nr}' Copied")
            page_nr += 1
            driver.execute_script("arguments[0].click();", element)

    except TimeoutException:
        print("Reached the last page.")
        driver.quit()
        return True, output_directory

    except NoSuchElementException:
        if max_attempts > 0:
            print("Element not found. Retrying...")
            return get_book_pages(driver=driver, book_url=book_url, output_directory=output_directory, page_nr=page_nr, max_attempts=max_attempts - 1)
        else:
            print("Max attempts reached. Exiting.")
            driver.quit()
            return False, None

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return False, None

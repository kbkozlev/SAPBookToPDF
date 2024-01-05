import os
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.helper.exceptions import LoginFailedError


def capture_book_pages(e_mail: str, passwd: str, book_url: str) -> bool:
    directory = 'files/rawPictures'
    if not os.path.exists(directory):
        os.makedirs(directory)

    desired_dpi = 2.0
    options = webdriver.ChromeOptions()
    options.add_argument(f"--force-device-scale-factor={desired_dpi}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.sap-press.com/accounts/login/?next=/")

    try:
        email_el = driver.find_element(By.ID, "id_login-username")
        email_el.send_keys(e_mail)
        password_el = driver.find_element(By.ID, "id_login-password")
        password_el.send_keys(passwd)
        login_button = driver.find_element(By.XPATH, "//button[@name='login_submit']")
        login_button.click()
        print("Logging in...")

        try:
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="login-input"]/div[1]')))
            raise LoginFailedError()
        except TimeoutException:
            print("Logged in successfully!")
            get_book_pages(driver=driver, book_url=book_url, directory=directory)

    except LoginFailedError as e:
        print(e)
        driver.quit()
        return False


def get_book_pages(driver, book_url, directory, page_nr=1, max_attempts=3) -> bool | tuple[bool, str]:

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
            driver.save_screenshot(f'{directory}/{str(page_nr).zfill(2)}.png')
            print(f"Page: '{page_nr}' Copied")
            page_nr += 1
            driver.execute_script("arguments[0].click();", element)

    except TimeoutException:
        print("Reached the last page.")
        driver.quit()
        return True, directory

    except NoSuchElementException:
        if max_attempts > 0:
            print("Element not found. Retrying...")
            return get_book_pages(driver, book_url, page_nr, max_attempts - 1)
        else:
            print("Max attempts reached. Exiting.")
            driver.quit()
            return False

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return False


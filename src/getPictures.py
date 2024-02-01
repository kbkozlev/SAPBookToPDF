import os
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def get_book_pages(book_url: str, driver: webdriver.Edge, page_nr: int = 1) -> tuple[bool, None, None] | tuple[bool, str, int]:
    """
    Creates a screenshot of every page of a book
    :param book_url: The URL of the book to be processed
    :param driver: Driver object
    :param page_nr: Page number used for the name of the screenshot
    :return:
    """
    output_folder = 'files/1.rawPictures'
    size = 0

    response = requests.get(book_url)
    if response.status_code == 200:
        os.makedirs(output_folder, exist_ok=True)

        try:
            print('\nNavigating to book...\n')
            driver.get(book_url)
        except Exception as e:
            print(f"Error: {e}")

    else:
        print(f"\nFailed to load the book page. Received status code: {response.status_code}")
        return False, None, None

    time.sleep(2)

    try:
        # decline last read page, and start from the beginning
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="lastReadPanel"]/a[2]'))).click()
    except TimeoutException:
        pass

    time.sleep(2)
    try:
        # Change size of book page to 4
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="reader_nav"]/ul/li[3]/ul/li[4]/a'))).click()
        size = 4
    except TimeoutException:
        try:
            # Change size of book page to 3
            WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="reader_nav"]/ul/li[3]/ul/li[3]/a'))).click()
            size = 3
        except TimeoutException:
            pass

    driver.set_window_size(1500, 1800)

    try:
        while True:
            # Click next-page button
            element = WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div[4]/div[1]/div[1]/ul/li[8]/a[2]/span')))

            time.sleep(4)  # timer to wait for the full loading of the page (adjust based on internet quality)
            image_name = f"{str(page_nr).zfill(2)}.png"
            driver.save_screenshot(f'{output_folder}/{image_name}')
            print(f"Image: '{image_name}' saved.")
            page_nr += 1
            driver.execute_script("arguments[0].click();", element)

    except TimeoutException:
        print(f"\nReached the last page, all pictures have been saved to folder '{output_folder}'.\n")
        return True, output_folder, size

    except Exception as e:
        print(f"\nError: {e}")
        return False, None, None

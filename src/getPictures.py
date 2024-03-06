import os
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.helper.identicalImages import are_images_identical
from src.helper.customExceptions import IdenticalImageError
from src.helper.removeDir import remove_directories
from advancedprinter import print


def get_book_pages(book_url: str, cover: str, driver: webdriver.Edge, page_nr: int = 1, max_tries: int = 1) -> tuple[bool, None, None] | tuple[bool, str, int]:
    """
    Creates a screenshot of every page of a book
    :param max_tries:
    :param cover: The url for the cover of the book
    :param book_url: The URL of the book to be processed
    :param driver: Driver object
    :param page_nr: Page number used for the name of the screenshot
    :return:
    """
    output_folder = 'files/1.rawPictures'
    downloaded_images = []
    size = 0

    try:
        book_response = requests.get(book_url)

        if book_response.status_code == 200:
            os.makedirs(output_folder, exist_ok=True)

            print(f'Navigating to book...\n', c='yellow2')
            #  Open book url
            driver.get(book_url)

            #  Fetch the cover of the book and download
            cover_response = requests.get(cover)
            cover_name = '00.png'
            if cover_response.status_code == 200:
                with open(f'{output_folder}/{cover_name}', 'wb') as file:
                    file.write(cover_response.content)
                print(f"Image: '{cover_name}' saved.")

        else:
            print(f'\nFailed to load the book page. Received status code: {book_response.status_code}', c='red')
            return False, None, None

    except Exception as e:
        if max_tries == 3:
            print(f'\nFailed to load the book page.', c='red')
            return False, None, None

        else:
            print(f'\nError: {e} retrying.\n', c='red')
            remove_directories()
            return get_book_pages(book_url=book_url, cover=cover, driver=driver, max_tries=max_tries + 1)

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

            if len(downloaded_images) >= 2:
                identical = are_images_identical(image1=downloaded_images[-2], image2=downloaded_images[-1])
                if identical:
                    raise IdenticalImageError

            # Find next page button
            element = WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div[4]/div[1]/div[1]/ul/li[8]/a[2]/span')))

            time.sleep(4)  # timer to wait for the full loading of the page (adjust based on internet quality)
            
            image_name = f"{str(page_nr).zfill(2)}.png"
            driver.save_screenshot(f'{output_folder}/{image_name}')
            downloaded_images.append(f'{output_folder}/{image_name}')
            print(f"Image: '{image_name}' saved.")
            page_nr += 1
            # Click next-page button
            driver.execute_script("arguments[0].click();", element)

    except TimeoutException:
        print(f"\nReached the last page, all pictures have been saved to folder '{output_folder}'.\n")
        return True, output_folder, size

    except IdenticalImageError as e:
        if max_tries == 3:
            return False, None, None

        else:
            print(f'\nError: {e} retrying.\n', c='red')
            remove_directories()
            return get_book_pages(book_url=book_url, cover=cover, driver=driver, max_tries=max_tries + 1)

    except Exception as e:
        print(f'\nError: {e}', c='red')
        return False, None, None

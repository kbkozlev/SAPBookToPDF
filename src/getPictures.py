import os
import time
import requests
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def get_book_pages(book_url, driver, page_nr=1, max_attempts=3) -> tuple[bool, str] | tuple[bool, None]:
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
        print("\nReached the last page.\n")
        return True, output_directory

    except NoSuchElementException:
        if max_attempts > 0:
            print("\nElement not found. Retrying...")
            return get_book_pages(book_url=book_url, driver=driver, page_nr=page_nr, max_attempts=max_attempts - 1)
        else:
            print("\nMax attempts reached. Exiting.")
            return False, None

    except Exception as e:
        print(f"\nError: {e}")
        return False, None

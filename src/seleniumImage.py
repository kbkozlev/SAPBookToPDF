from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time
import os


class LoginFailedError(Exception):
    def __init__(self, message="Login failed!"):
        self.message = message
        super().__init__(self.message)


def capture_book_pages(book_url: str) -> bool | None:
    """
    This function makes a screenshot of every page of a provided book
    :param book_url:  URL in the SAP Press Library
    :return:
    """

    directory = 'files/rawPictures'
    if not os.path.exists(directory):
        os.makedirs(directory)

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    desired_dpi = 2.0
    options = webdriver.ChromeOptions()
    options.add_argument(f"--force-device-scale-factor={desired_dpi}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.sap-press.com/accounts/login/?next=/")

    # Login
    try:
        email_el = driver.find_element(By.ID, "id_login-username")
        email_el.send_keys(email)
        password_el = driver.find_element(By.ID, "id_login-password")
        password_el.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//button[@name='login_submit']")
        login_button.click()
        print("Logging in...")

        try:
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="login-input"]/div[1]')))
            raise LoginFailedError()
        except TimeoutException:
            print("Logged in successfully!")

    except LoginFailedError as e:
        print(e)
        driver.quit()
        return False

    # Navigate to book
    driver.get(book_url)
    if driver.find_element(By.CLASS_NAME, "errorpage"):
        print("Page not found!")
        return False

    # Remove last position message and go full screen
    try:
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="lastReadPanel"]/a[2]'))).click()
    except TimeoutException:
        pass

    try:
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="reader_nav"]/ul/li[3]/ul/li[4]/a'))).click()
    except TimeoutException:
        pass

    driver.set_window_size(1500, 1800)

    page_nr = 1
    while True:
        try:
            # Wait for the element to be present and visible
            element = WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//*[@id="reader_nav"]/ul/li[8]/a[2]')))

            time.sleep(2)
            driver.save_screenshot(f'rawPictures/{str(page_nr).zfill(2)}.png')
            print(f"Page: {page_nr} Copied")
            page_nr += 1

            # Execute JavaScript to click the next page element
            driver.execute_script("arguments[0].click();", element)

        except Exception as e:
            print(f"Error: {e}")
            driver.quit()
            return False
        finally:
            break

    driver.quit()

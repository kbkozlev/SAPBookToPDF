import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.helper.customExceptions import LoginFailedError


def init_books(e_mail: str, passwd: str, driver: webdriver.Edge) -> tuple[bool, list] | tuple[bool, None]:
    """
    Initialises the list of books to be processed.
    Calls the "login" function and the "list creation" function.
    Waits for person to confirm the list of books to be processed.

    :param e_mail: E-mail is passed to the login function.
    :param passwd: Password is passed to the login function
    :param driver: Driver object
    :return:
    """
    logged_in = login_sap_press(email=e_mail, passwd=passwd, driver=driver)

    if logged_in:
        success, book_list = get_book_list(driver=driver)
        if len(book_list) == 0:
            print("\nNo Books found!")
            return False, None

        cont = input("\nContinue: y/n? ")
        if cont.lower() in ["y", ""]:
            return success, book_list if success else (False, None)
        else:
            print("\nExiting...")
    return False, None


def login_sap_press(email: str, passwd: str, driver: webdriver.Edge, max_retries: int = 3) -> bool:
    """
    Handles the logging in to the website with retry mechanism
    :param email: E-mail to be used for signing in
    :param passwd: Password to be used for signing in
    :param driver: Driver object
    :param max_retries: Maximum number of login retry attempts
    :return: True if login is successful, False otherwise
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Logging in (Attempt {attempt}/{max_retries})...")

            driver.get("https://www.sap-press.com/accounts/login/?next=/")
            driver.find_element(By.ID, "id_login-username").send_keys(email)
            driver.find_element(By.ID, "id_login-password").send_keys(passwd)
            driver.find_element(By.XPATH, "//button[@name='login_submit']").click()

            # Waits for the 'login failed' page to appear; raises TimeoutException if it doesn't
            try:
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="login-input"]/div[1]')))
                raise LoginFailedError("Login failed!")

            except TimeoutException:
                # If no TimeoutException is raised, it means the login was successful
                print("\nLogged in successfully!\n")
                return True

        except NoSuchElementException as e:
            failed_element = e.msg
            print(f"Login failed - {failed_element}\n")

        except LoginFailedError as e:
            print(e)

            if attempt == max_retries:
                return False

        except Exception as e:
            print(f"Login failed - Unexpected error: {e}")

    return False


def get_book_list(driver: webdriver.Edge) -> tuple[bool, None] | tuple[bool, list]:
    """
    For all elements with class "product-detail" in the page,
    it fetches the "name" and "href" element and stores them in a list of dictionaries
    :param driver: Driver object
    :return:
    """
    driver.get("https://library.sap-press.com/library/")
    result_list = []

    try:
        product_details = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "product-detail")))

        for product_detail in product_details:
            title_element = product_detail.find_element(By.CLASS_NAME, "titel")
            title = re.sub(r"[^a-zA-Z0-9\s]", '', title_element.text.strip())
            href = title_element.find_element(By.CSS_SELECTOR, "a.read-link").get_attribute('href')

            result_dict = {'title': title, 'href': href}
            result_list.append(result_dict)
            print(f"Book: '{title}' added to list.")

        return True, result_list

    except TimeoutException:
        try:
            driver.find_element(By.CLASS_NAME, "product-detail")
        except NoSuchElementException as e:
            print(e.msg)
            return False, result_list

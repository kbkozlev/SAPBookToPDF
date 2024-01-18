import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from src.helper.customExceptions import LoginFailedError


def init_books(e_mail: str, passwd: str, driver) -> tuple[bool, list] | tuple[bool, None]:
    logged_in = login_sap_press(e_mail=e_mail, passwd=passwd, driver=driver)

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


def login_sap_press(e_mail: str, passwd: str, driver) -> bool:
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
        # driver.quit()
        return False

    except Exception:
        raise LoginFailedError


def get_book_list(driver) -> tuple[bool, None] | tuple[bool, list]:
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

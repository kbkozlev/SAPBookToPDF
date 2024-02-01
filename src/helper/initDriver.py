from selenium import webdriver

# Edge Import
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from contextlib import contextmanager


@contextmanager
def init_driver() -> webdriver.Edge:
    """
    Initiates the Selenium "Edge" driver that is going to be used.
    :return: WebDriver instance
    """
    desired_dpi = 2.0
    options = webdriver.EdgeOptions()
    options.add_argument(f"--force-device-scale-factor={desired_dpi}")
    options.add_argument("--inprivate")
    # options.add_argument("--headless")

    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    try:
        yield driver
    finally:
        driver.quit()


def open_new_tab(driver):
    # Execute JavaScript to open a new tab
    driver.execute_script("window.open('', '_blank');")

    # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[-1])


def close_current_tab(driver):
    # Close the current tab using JavaScript
    driver.execute_script("window.close();")

    # Switch back to the main tab
    driver.switch_to.window(driver.window_handles[0])
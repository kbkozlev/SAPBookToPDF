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
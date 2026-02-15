import uuid

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from locators import BUTTON_ARROW_RIGHT_XPATH


def unique_email():
    return f"{uuid.uuid4()}@example.com"


def click_safely(browser, xpath):
    for _ in range(10):
        try:
            browser.find_element(By.XPATH, xpath).click()
            break
        except StaleElementReferenceException:
            pass


def go_to_last_page(browser):
    next_page_button = WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, BUTTON_ARROW_RIGHT_XPATH))
    )
    is_last_page = not next_page_button.is_enabled()
    while not is_last_page:
        next_page_button.click()
        next_page_button = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, BUTTON_ARROW_RIGHT_XPATH))
        )
        is_last_page = not next_page_button.is_enabled()
    click_safely(browser, BUTTON_ARROW_RIGHT_XPATH)

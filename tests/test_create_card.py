import uuid

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from locators import (
    BUTTON_POST_CARD_XPATH,
    H1_AUTHORIZATION_REQUIRED_TO_POST_CARD_XPATH,
    BUTTON_LOGIN_REGISTRATION_XPATH,
    INPUT_EMAIL_XPATH,
    INPUT_PASSWORD_XPATH,
    BUTTON_LOGIN_XPATH,
    INPUT_CARD_NAME_XPATH,
    TEXTAREA_CARD_DESCRIPTION_XPATH,
    INPUT_CARD_PRICE_XPATH,
    BUTTON_PROFILE_XPATH,
    DIV_MY_CARDS_XPATH,
    DIV_CARD_XPATH,
    BUTTON_PUBLISH_XPATH,
    BUTTON_ARROW_RIGHT_XPATH
)
from test_data import MAIN_URL, CREATE_LISTING_URL, EXISTING_USER_EMAIL, TEST_PASSWORD


def test_unauthorized_user_posting_card(browser):
    browser.get(MAIN_URL)

    browser.find_element(By.XPATH, BUTTON_POST_CARD_XPATH).click()
    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, H1_AUTHORIZATION_REQUIRED_TO_POST_CARD_XPATH))
    )
    modal_title = browser.find_element(By.XPATH, H1_AUTHORIZATION_REQUIRED_TO_POST_CARD_XPATH)

    assert modal_title.text == "Чтобы разместить объявление, авторизуйтесь"


def test_authorized_user_posting_card(browser):
    browser.get(MAIN_URL)

    # логин
    browser.find_element(By.XPATH, BUTTON_LOGIN_REGISTRATION_XPATH).click()
    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, INPUT_EMAIL_XPATH))
    ).send_keys(EXISTING_USER_EMAIL)
    browser.find_element(By.XPATH, INPUT_PASSWORD_XPATH).send_keys(TEST_PASSWORD)
    browser.find_element(By.XPATH, BUTTON_LOGIN_XPATH).click()

    # создаём карточку
    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, BUTTON_PROFILE_XPATH))
    )
    browser.find_element(By.XPATH, BUTTON_POST_CARD_XPATH).click()
    unique_card_name = str(uuid.uuid4())
    browser.find_element(By.XPATH, INPUT_CARD_NAME_XPATH).send_keys(unique_card_name)
    browser.find_element(By.XPATH, TEXTAREA_CARD_DESCRIPTION_XPATH).send_keys("Тестовое описание")
    browser.find_element(By.XPATH, INPUT_CARD_PRICE_XPATH).send_keys("1000")
    browser.find_element(By.XPATH, BUTTON_PUBLISH_XPATH).click()

    # проверяем наличие карточки в профиле
    WebDriverWait(browser, 5).until(
        ec.url_changes(CREATE_LISTING_URL)
    )
    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_PROFILE_XPATH))
    )
    __click_safely(browser, BUTTON_PROFILE_XPATH)
    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, DIV_MY_CARDS_XPATH))
    )
    __go_to_last_page(browser)
    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, DIV_MY_CARDS_XPATH))
    )
    cards = list(filter(lambda x: unique_card_name in x.text, browser.find_elements(By.XPATH, DIV_CARD_XPATH)))

    assert len(cards) > 0
    assert cards[0].is_displayed()


def __click_safely(browser, xpath):
    for _ in range(10):
        try:
            browser.find_element(By.XPATH, xpath).click()
            break
        except StaleElementReferenceException:
            pass

def __go_to_last_page(browser):
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
    __click_safely(browser, BUTTON_ARROW_RIGHT_XPATH)
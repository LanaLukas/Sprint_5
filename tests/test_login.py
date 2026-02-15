from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from locators import (
    BUTTON_LOGIN_REGISTRATION_XPATH,
    BUTTON_LOGIN_XPATH,
    INPUT_EMAIL_XPATH,
    INPUT_PASSWORD_XPATH,
    BUTTON_PROFILE_XPATH,
    H3_PROFILE_TEXT_NAME_XPATH
)
from test_data import TEST_PASSWORD, EXISTING_USER_EMAIL
from test_pages import MAIN_URL


class TestLogin:

    def test_user_login(self, browser):
        browser.get(MAIN_URL)

        WebDriverWait(browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, BUTTON_LOGIN_REGISTRATION_XPATH))
        ).click()
        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, INPUT_EMAIL_XPATH))
        ).send_keys(EXISTING_USER_EMAIL)
        browser.find_element(By.XPATH, INPUT_PASSWORD_XPATH).send_keys(TEST_PASSWORD)
        browser.find_element(By.XPATH, BUTTON_LOGIN_XPATH).click()

        WebDriverWait(browser, 5).until(
            ec.url_contains(MAIN_URL)
        )
        avatar_element = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, BUTTON_PROFILE_XPATH))
        )
        user_name_element = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, H3_PROFILE_TEXT_NAME_XPATH))
        )

        assert MAIN_URL in browser.current_url, "Должны находиться на главной странице после входа"
        assert user_name_element.text == "User.", "Имя пользователя должно быть User."
        assert avatar_element.is_displayed(), "Аватар должен быть видимым"

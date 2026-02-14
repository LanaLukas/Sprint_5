from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from locators import (
    BUTTON_LOGIN_REGISTRATION_XPATH,
    BUTTON_NO_ACCOUNT_XPATH,
    INPUT_EMAIL_XPATH,
    INPUT_ERROR_MESSAGE_XPATH,
    INPUT_PASSWORD_XPATH,
    INPUT_REPEAT_PASSWORD_XPATH,
    BUTTON_CREATE_ACCOUNT_XPATH,
    BUTTON_PROFILE_XPATH,
    H3_PROFILE_TEXT_NAME_XPATH
)
from test_data import MAIN_AFTER_REGISTRATION_URL, MAIN_URL, TEST_PASSWORD, ERROR_FORM_COLOR, EXISTING_USER_EMAIL


def test_user_registration(browser, unique_email):
    browser.get(MAIN_URL)

    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_LOGIN_REGISTRATION_XPATH))
    ).click()
    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_NO_ACCOUNT_XPATH))
    ).click()

    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, INPUT_EMAIL_XPATH))
    ).send_keys(unique_email)
    browser.find_element(By.XPATH, INPUT_PASSWORD_XPATH).send_keys(TEST_PASSWORD)
    browser.find_element(By.XPATH, INPUT_REPEAT_PASSWORD_XPATH).send_keys(TEST_PASSWORD)
    browser.find_element(By.XPATH, BUTTON_CREATE_ACCOUNT_XPATH).click()

    WebDriverWait(browser, 5).until(
        ec.url_to_be(MAIN_AFTER_REGISTRATION_URL)
    )
    avatar_element = WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, BUTTON_PROFILE_XPATH))
    )
    user_name_element = WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, H3_PROFILE_TEXT_NAME_XPATH))
    )

    assert MAIN_AFTER_REGISTRATION_URL == browser.current_url, "Должны находиться на главной странице после регистрации"
    assert user_name_element.text == "User.", "Имя пользователя должно быть User."
    assert avatar_element.is_displayed(), "Аватар должен быть видимым"


def test_user_registration_validation_wrong_email_format(browser):
    browser.get(MAIN_URL)

    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_LOGIN_REGISTRATION_XPATH))
    ).click()
    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_NO_ACCOUNT_XPATH))
    ).click()
    browser.find_element(By.XPATH, BUTTON_CREATE_ACCOUNT_XPATH).click()

    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, INPUT_EMAIL_XPATH))
    ).send_keys("wrongmail")
    email_input_parent = browser.find_element(By.XPATH, f'{INPUT_EMAIL_XPATH}/..')
    password_input_parent = browser.find_element(By.XPATH, f'{INPUT_PASSWORD_XPATH}/..')
    repeat_password_input_parent = browser.find_element(By.XPATH, f'{INPUT_REPEAT_PASSWORD_XPATH}/..')
    error_message = WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, INPUT_ERROR_MESSAGE_XPATH))
    )
    email_border_color = email_input_parent.value_of_css_property('border-color')
    password_border_color = password_input_parent.value_of_css_property('border-color')
    repeat_password_border_color = repeat_password_input_parent.value_of_css_property('border-color')

    assert ERROR_FORM_COLOR == email_border_color, "Поле Введите Email должно быть выделено красным"
    assert ERROR_FORM_COLOR == password_border_color, "Поле Пароль должно быть выделено красным"
    assert ERROR_FORM_COLOR == repeat_password_border_color, "Поле Повторите пароль должно быть выделено красным"
    assert error_message.is_displayed(), "Должно отображаться сообщение об ошибке"


def test_user_registration_existing_user(browser):
    browser.get(MAIN_URL)

    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_LOGIN_REGISTRATION_XPATH))
    ).click()
    WebDriverWait(browser, 5).until(
        ec.element_to_be_clickable((By.XPATH, BUTTON_NO_ACCOUNT_XPATH))
    ).click()
    WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, INPUT_EMAIL_XPATH))
    ).send_keys(EXISTING_USER_EMAIL)
    browser.find_element(By.XPATH, INPUT_PASSWORD_XPATH).send_keys(TEST_PASSWORD)
    browser.find_element(By.XPATH, INPUT_REPEAT_PASSWORD_XPATH).send_keys(TEST_PASSWORD)
    browser.find_element(By.XPATH, BUTTON_CREATE_ACCOUNT_XPATH).click()

    email_input_parent = browser.find_element(By.XPATH, f'{INPUT_EMAIL_XPATH}/..')
    password_input_parent = browser.find_element(By.XPATH, f'{INPUT_PASSWORD_XPATH}/..')
    repeat_password_input_parent = browser.find_element(By.XPATH, f'{INPUT_REPEAT_PASSWORD_XPATH}/..')
    error_message = WebDriverWait(browser, 5).until(
        ec.presence_of_element_located((By.XPATH, INPUT_ERROR_MESSAGE_XPATH))
    )
    email_border_color = email_input_parent.value_of_css_property('border-color')
    password_border_color = password_input_parent.value_of_css_property('border-color')
    repeat_password_border_color = repeat_password_input_parent.value_of_css_property('border-color')

    assert ERROR_FORM_COLOR == email_border_color, "Поле Введите Email должно быть выделено красным"
    assert ERROR_FORM_COLOR == password_border_color, "Поле Пароль должно быть выделено красным"
    assert ERROR_FORM_COLOR == repeat_password_border_color, "Поле Повторите пароль должно быть выделено красным"
    assert error_message.is_displayed(), "Должно отображаться сообщение об ошибке"

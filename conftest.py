import pytest
import uuid
from selenium import webdriver


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def unique_email():
    return f"{uuid.uuid4()}@example.com"

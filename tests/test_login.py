import pytest
from pages.login_page import LoginPage


def test_successful_login(driver):
    """Verifies that a user can successfully log in with valid credentials."""
    login_page = LoginPage(driver)

    # 1. Navigate to the application
    login_page.navigate_to("https://www.saucedemo.com/")

    # 2. Perform actions
    login_page.login_to_application("standard_user", "secret_sauce")

    # 3. Verify assertions
    assert "inventory.html" in driver.current_url


def test_invalid_login_error(driver):
    """Verifies that an appropriate error message is shown with bad credentials."""
    login_page = LoginPage(driver)

    login_page.navigate_to("https://www.saucedemo.com/")
    login_page.login_to_application("locked_out_user", "wrong_password")

    error_text = login_page.get_error_message()
    assert "Username and password do not match" in error_text
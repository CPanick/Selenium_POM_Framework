from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Locators defined as private class tuples (Strategy, Value)
        self._username_field = (By.ID, "user-name")
        self._password_field = (By.ID, "password")
        self._login_button = (By.ID, "login-button")
        self._error_container = (By.CSS_SELECTOR, "h3[data-test='error']")

    def login_to_application(self, username, password):
        """Performs the complete login action sequence."""
        self.enter_text(self._username_field, username)
        self.enter_text(self._password_field, password)
        # The * operator unpacks the tuple into (By.ID, "login-button")
        self.click_element(self._login_button)

    def get_error_message(self):
        """Returns error text if login fails."""
        return self.get_text(self._error_container)
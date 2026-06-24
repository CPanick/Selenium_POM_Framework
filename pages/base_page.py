from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def navigate_to(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        """Waits for an element to be visible in the DOM before returning it."""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click_element(self, locator):
        """Waits for an element to be clickable, then clicks it."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text):
        """Waits for an element, clears any pre-existing text, and types into it."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Retrieves the inner text of an element."""
        return self.find_element(locator).text

    def get_page_title(self):
        """Retrieves the current page title."""
        return self.driver.title
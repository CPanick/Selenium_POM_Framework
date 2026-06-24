import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and teardown the Selenium WebDriver.
    Yields the driver instance to the test case.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    if os.environ.get("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # WebDriver Manager automatically downloads and matches the correct ChromeDriver binary
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver  # The test executes here

    driver.quit()  # Teardown: Ensures browser closes even if tests fail


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    An internal Pytest hook that executes after every phase of a test
    (setup, call/execution, and teardown).
    """
    # 1. Let the test phase execute completely first
    outcome = yield
    rep = outcome.get_result()

    # 2. Check if the test failed specifically during its execution phase ('call')
    if rep.when == "call" and rep.failed:
        try:
            # 3. Dynamically extract the 'driver' fixture from the running test
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]

                # 4. Create a folder named 'screenshots' if it doesn't exist
                os.makedirs("screenshots", exist_ok=True)

                # 5. Generate a clean, unique filename using the test name and a timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                clean_test_name = item.name.replace("[", "_").replace("]", "_")
                filename = f"screenshots/{clean_test_name}_{timestamp}.png"

                # 6. Save the screenshot via Selenium
                driver.save_screenshot(filename)
                print(f"\n[FAILURE DETECTED] Saved failure screenshot to: {filename}")

        except Exception as e:
            print(f"\nFailed to capture failure screenshot: {e}")
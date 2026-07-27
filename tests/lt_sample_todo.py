import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("driver")
class TestSeleniumPlayground:

    @pytest.mark.order(1)
    def test_simple_form_demo(self, driver):
        driver.get("https://testmuai.com/selenium-playground/simple-form-demo")

        message = "Welcome to TestMu AI"

        input_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-message"))
        )
        input_box.clear()
        input_box.send_keys(message)

        driver.find_element(By.ID, "showInput").click()

        output = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "message"))
        ).text

        assert output == message

    @pytest.mark.order(2)
    def test_simple_form_demo_second(self, driver):
        driver.get("https://testmuai.com/selenium-playground/simple-form-demo")

        message = "HyperExecute Rocks!"

        input_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-message"))
        )
        input_box.clear()
        input_box.send_keys(message)

        driver.find_element(By.ID, "showInput").click()

        output = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "message"))
        ).text

        assert output == message
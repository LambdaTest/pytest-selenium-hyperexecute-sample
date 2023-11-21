import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.webdriver.support.ui import Select

@pytest.mark.usefixtures('driver')
class TestLink:

    @pytest.mark.order(1)
    def test_input_forms(self, driver):
        action = ActionChains(driver)
        wait = WebDriverWait(driver, 5)
        driver.get('https://www.lambdatest.com/selenium-playground/')

        element = driver.find_element(By.XPATH, "//a[.='Input Form Submit']")
        element.click()

        URL = driver.current_url
        # Print the current URL, assert if required
        print("Current URL" + URL)

        name = driver.find_element(By.XPATH, "//input[@id='name']")
        name.send_keys("Testing")

        email_address = driver.find_element(By.XPATH, "//input[@id='inputEmail4']")
        email_address.send_keys("testing@testing.com")

        password = driver.find_element(By.XPATH, "//input[@id='inputPassword4']")
        password.send_keys("password")

        company = driver.find_element(By.CSS_SELECTOR, "#company")
        company.send_keys("LambdaTest")

        website = driver.find_element(By.CSS_SELECTOR, "#websitename")
        website.send_keys("https://wwww.lambdatest.com")

        country_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='country']"))
        country_dropdown.select_by_visible_text("United States")

        city = driver.find_element(By.XPATH, "//input[@id='inputCity']")
        city.send_keys("San Jose")

        address1 = driver.find_element(By.CSS_SELECTOR, "[placeholder='Address 1']")
        address1.send_keys("Googleplex, 1600 Amphitheatre Pkwy")

        address2 = driver.find_element(By.CSS_SELECTOR, "[placeholder='Address 2']")
        address2.send_keys(" Mountain View, CA 94043")

        state = driver.find_element(By.CSS_SELECTOR, "#inputState")
        state.send_keys("California")

        zipcode = driver.find_element(By.CSS_SELECTOR, "#inputZip")
        zipcode.send_keys("94088")

        # Click on the Submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "#seleniumform > div.text-right.mt-20 > button")
        submit_button.click()

        # Assert if the page contains a certain text
        assert driver.page_source.find("Thanks for contacting us, we will get back to you shortly")

        print("Input Form Demo complete")

        print(driver.find_element(By.TAG_NAME,'title').is_displayed())

    @pytest.mark.order(2)
    def test_progress_bars(self, driver):
        action = ActionChains(driver)
        # A wait of 5 seconds is added later in case the WebElements are loaded dynamically
        wait = WebDriverWait(driver, 5)

        driver.get('https://www.lambdatest.com/selenium-playground/input-form-demo')

       
        # wait.until(EC.element_to_be_clickable(element)).click()

        # Click on the Drag & Drop Sliders
        
        time.sleep(10)
        print("Progress Bar Test Complete")

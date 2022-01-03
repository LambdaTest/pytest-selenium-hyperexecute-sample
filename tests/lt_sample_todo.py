import pytest
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures('driver')
class TestLink:
    def test_title(self, driver):
        driver.get('https://lambdatest.github.io/sample-todo-app/')
        driver.find_element_by_name("li1").click()
        driver.find_element_by_name("li2").click()

        title = "Sample page - lambdatest.com"
        assert title == driver.title


    def test_item(self, driver):
        driver.get('https://lambdatest.github.io/sample-todo-app/')
        sample_text = "Happy Testing at LambdaTest"
        email_text_field = driver.find_element_by_id("sampletodotext")
        email_text_field.send_keys(sample_text)

        driver.find_element_by_id("addbutton").click()

        li6 = driver.find_element_by_name("li6")
        sys.stderr.write('li6')
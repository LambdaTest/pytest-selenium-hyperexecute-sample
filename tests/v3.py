import unittest
import json
import random
import logging
import os
import time
from os import environ
import argparse
import pytz
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# Options for different browsers
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

# Set up logging
logging.basicConfig(filename='test_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# Add a StreamHandler to print to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Assuming 'ist' is a timezone object you have defined or imported
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist) + timedelta(minutes=15)
formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Run selenium tests.')
parser.add_argument('--builds', type=int, default=1, help='The number of builds to run.')
parser.add_argument('--parallel', type=int, default=1, help='The maximum number of worker threads.')
parser.add_argument('--test_name', type=str, default=f"atxHYE_flakyTest_{formatted_current_time}", help='The base name of the test.')
parser.add_argument('--build_name', type=str, default=f"atxHYE_flakyBuild_{formatted_current_time}", help='The base name of the build.')
parser.add_argument('--username', type=str, default= os.environ.get("LT_USERNAME") , help='The username to use for the selenium tests.')
parser.add_argument('--access_key', type=str, default = os.environ.get("LT_ACCESS_KEY"), help='The access key to use for the selenium tests.')
parser.add_argument('--env', type=str, default="prod", choices=["stage", "prod"], help='The environment to run the tests in. Default is stage.')
parser.add_argument('--hub_url', type=str, default="hub", help='The hub url to use for the selenium tests.')

parser.add_argument('--command_count', type=int, default=0, help='To increase command count in the test by factor of 8')
parser.add_argument('--error_commands', type=int, default=0, help='To include error commands in the test, maximum value that can be passed is 15')
parser.add_argument('--error_repeat', type=int, default=1, help='To run the chosen error n number of times')
parser.add_argument('--build_tags', type=str, default="", help='Build tags to include in the test. Comma separated.')
parser.add_argument('--test_tags', type=str, default="", help='Test tags to include in the test. Comma separated.')
parser.add_argument('--caps_json', type=str, default='capsV3.json', help='Path to the caps json file.')
parser.add_argument('--project', type=str, default='ATXproject', help='The project name for the selenium tests.')


args = parser.parse_args()

# convert comma-separated strings into lists
args.username = [user.strip() for user in args.username.split(',')]
args.access_key = [key.strip() for key in args.access_key.split(',')]
args.build_tags = [tag.strip() for tag in args.build_tags.split(',')] if args.build_tags else []
args.test_tags = [tag.strip() for tag in args.test_tags.split(',')] if args.test_tags else []

class FirstSampleTest(unittest.TestCase):

    # with open('capsV3.json') as json_file:
    #     CAPS = json.load(json_file)
    with open(args.caps_json) as json_file:
        CAPS = json.load(json_file)



    def run_demo_site_test(self, build_num, test_id, capabilities, command_count, error_commands, error_repeat,  username, access_key):
        try:
            lt_options = {
                # "username": args.username,
                # "accessKey": args.access_key,
                "username": username,
                "accessKey": access_key,                
                "network": capabilities.get('network'),
                "build": f"{args.build_name}_{build_num}",
                "name": f"{args.test_name}",#_{build_num}",
                "console": capabilities.get('console'),
                "w3c": True,
                "plugin": "python-python",
                "platform" : capabilities.get('platformName'),
                "buildTags": args.build_tags,
		        "tags": args.test_tags,
                "resolution": capabilities.get('resolution'),
                "project": args.project
            }

            # Construct hub url
            base_url = f"{args.hub_url}.lambdatest.com" if args.env == "prod" else f"stage-{args.hub_url}.lambdatestinternal.com"

            # Decide which browser to use based on the browserName in desired capabilities
            browserName = capabilities.get('browserName').lower()
            if browserName == 'chrome':
                options = ChromeOptions()
            elif browserName == 'firefox':
                options = FirefoxOptions()
            elif browserName == 'edge':
                options = EdgeOptions()
            elif browserName == 'safari':
                options = SafariOptions()
            else:
                raise ValueError('Unsupported browser: ' + browserName)

            options.browser_version = capabilities.get('browserVersion')
            # options.platform_name = capabilities.get('platformName')

            options.set_capability('LT:Options', lt_options)
            # print(f'"http://{username}:{access_key}@{base_url}/wd/hub')
            driver = webdriver.Remote(
                command_executor=f"http://{username}:{access_key}@{base_url}/wd/hub",
                options=options)

            driver.set_page_load_timeout(30)
            driver.set_window_size(1920, 1080)

            logger.debug(f'Running test {test_id} for build {build_num}')
            driver.get("https://stage-lambda-devops-use-only.lambdatestinternal.com/To-do-app/index.html")

            if command_count>0:
                for i in range(command_count):
                    driver.find_element(By.NAME, "li1").click()
                    driver.find_element(By.NAME, "li2").click()

                for i in range(command_count):
                    driver.find_element(By.ID, "sampletodotext").send_keys(f"LambdaTest {i}")
                    add_button = driver.find_element(By.ID, "addbutton")
                    add_button.click()

            errorFunctions = [
                lambda: ( driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'), driver.get('http://www.lambdatest.com'), driver.set_page_load_timeout(1), driver.get('http://www.youtube.com')),
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'),driver.set_page_load_timeout(30), driver.get('http://www.google.com'), driver.find_element(By.NAME, 'btnK').click()),#element not interactable
                # lambda: (driver.get('http://www.google.com'), driver.find_element(By.NAME, 'noSuchElement').click()),
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'), driver.get('http://www.lambdatest.com'),ActionChains(driver).move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), 9999999, 9999999).perform()),
                # lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'),driver.set_page_load_timeout(30), driver.get('http://www.google.com'), search_field := driver.find_element(By.CLASS_NAME,'gLFyf'), driver.execute_script("argument[0].value='LambdaTest';", search_field)),#JSError
                lambda: (driver.set_page_load_timeout(30), driver.get('http://www.google.com'),driver.find_element(By.CLASS_NAME,'gLFyf').send_keys('LambdaTest'), driver.find_element(By.XPATH,"(//input[@name='btnK'])[2]").click()),#ElementClickIntercepted
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'), driver.get('http://www.lambdatest.com'), driver.get('http://www.google.com'),driver.find_element(By.CLASS_NAME, 123)),#InvalidSelector
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'), driver.get('http://www.lambdatest.com'), driver.get('http://www.google.com'),driver.add_cookie({"name" : "cookie_name", "value" : "cookie_value", "domain" : "wrong.domain.com"})),#InvalidCookieDomain
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'),driver.set_page_load_timeout(30), driver.get('http://www.google.com'), driver.find_element(By.NAME, 'btnI').clear()),#InvalidElementState
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'), driver.get('http://www.lambdatest.com'), driver.get('http://www.google.com'),driver.switch_to.alert),#noSuchAlert
                lambda: driver.switch_to.window('non_existent_window'),#noSuchWindow
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'), driver.get('http://www.lambdatest.com'), driver.get('http://www.google.com'),driver.switch_to.frame(1)),#noSuchFrame
                # lambda: (driver.get('http://www.google.com'),driver.set_page_load_timeout(30), driver.get('http://www.google.com'), old_page:= driver.find_element(By.NAME, 'q'), driver.refresh(), old_page.click()),#StaleElementReference
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'),driver.get('http://www.google.com'),driver.set_page_load_timeout(30), driver.get('http://www.google.com'), driver.get_cookie('abd'), driver.add_cookie({"name": "foo", "value": "bar"}), driver.get_cookie('foo') ),#NoSuchCookie
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'),driver.set_page_load_timeout(30), driver.get('http://www.google.com'), driver.add_cookie({"name" : "", "value" : ""})),#UnabletoSetCookie
                lambda: (driver.get('http://www.google.com'),driver.get('http://www.youtube.com'), driver.get('http://www.google.com'),driver.set_page_load_timeout(30),  driver.execute_script("alert('Hello from Selenium!');"),driver.get('http://www.google.com')),#UnexpectedAlertOpen
                ]
            
            if error_commands>0:
                chosen_error_commands = random.sample(errorFunctions, error_commands)

                for command in chosen_error_commands:
                    for i in range(error_repeat):
                        try:
                            driver.get('http://www.google.com')
                            driver.get('http://www.youtube.com')
                            command()
                        except Exception as e:
                            logger.error(f"An error occurred: {e}")

            driver.get("https://stage-lambda-devops-use-only.lambdatestinternal.com/To-do-app/index.html")

            driver.find_element(By.NAME, "li1").click()
            driver.find_element(By.NAME, "li2").click()
            logger.debug("Clicked on the second element")

            driver.find_element(By.ID, "sampletodotext").send_keys("LambdaTest")
            add_button = driver.find_element(By.ID, "addbutton")

            attempts = 2
            for attempt in range(attempts):
                try:
                    add_button.click()
                    driver.find_element(By.ID, "addbutton")
                    logger.info("Added LambdaTest checkbox")
                    break
                except WebDriverException as e:
                    logger.error(f"Attempt {attempt + 1} failed. Retrying...")
                    if attempt == attempts - 1:
                        logger.error(e, exc_info=True)

            search = driver.find_element(By.CSS_SELECTOR, ".container h2")
            assert search.is_displayed(), "heading is not displayed"
            search.click()
            driver.implicitly_wait(3)

            heading = driver.find_element(By.CSS_SELECTOR, ".container h2")

            # Passed Build
            if heading.is_displayed():
                heading.click()
                if test_id <2:
                    # driver.execute_script("window.alert('Passing command before idle timeout')")
                    driver.find_element(By.ID, "addbutton")
                    driver.execute_script("lambda-status=passed")
                    # driver.execute_script("lambda-status=passed")
                    logger.info("Test marked as passed.")
                elif 2 <= test_id < 4:
                    try:
                        driver.find_element(By.ID, "non_existent_element")
                    except WebDriverException:
                        logger.error("Failing command executed.")
                    driver.execute_script("lambda-status=failed")
                    # driver.execute_script("lambda-status=passed")
                    logger.info("Test marked as failed.")
                elif 4 <= test_id < 6:
                    try:
                        driver.find_element(By.ID, "addbutton")
                        # driver.execute_script("lambda-status=failed")
                        driver.execute_script("lambda-status=passed")
                        # driver.find_element(By.ID, "addbutton2")
                    except WebDriverException:
                        logger.error("Element not found, moving on to quit the browser.")  # This command will fail, making the test flaky
                elif 6 <= test_id < 8:
                    try:
                        driver.find_element(By.ID, "addbutton2")
                        # driver.execute_script("lambda-status=passed")
                        # driver.find_element(By.ID, "addbutton2")
                    except WebDriverException:
                        logger.error("Element not found, moving on to quit the browser.")  # This command will fail, making the test flaky
                    driver.execute_script("lambda-status=failed")
                elif 8 <= test_id < 10:
                    try:
                        driver.find_element(By.ID, "addbutton")
                        # driver.execute_script("lambda-status=failed")
                        driver.execute_script("lambda-status=passed")
                        # driver.find_element(By.ID, "addbutton2")
                    except WebDriverException:
                        logger.error("Element not found, moving on to quit the browser.")  # This command will fail, making the test flaky
                elif 10 <= test_id < 12:
                    try:
                        driver.find_element(By.ID, "addbutton2")
                        # driver.execute_script("lambda-status=passed")
                        # driver.find_element(By.ID, "addbutton2")
                    except WebDriverException:
                        logger.error("Element not found, moving on to quit the browser.")  # This command will fail, making the test flaky
                    driver.execute_script("lambda-status=failed")

                else:
                    # driver.implicitly_wait(2)
                    try:
                        driver.find_element(By.ID, "addbutton")
                        # driver.execute_script("lambda-status=failed")
                        driver.execute_script("lambda-status=passed")
                        # driver.find_element(By.ID, "addbutton2")
                        logger.info("Test marked as completed.")
                    except WebDriverException:
                        logger.error("Element not found, moving on to quit the browser.")
        finally:
            driver.quit()

            
    def _test_single_build(self, build_num, username, access_key):
        command_count = args.command_count
        error_commands = args.error_commands
        error_repeat = args.error_repeat
        for test_id, capabilities in enumerate(self.CAPS):
            self.run_demo_site_test(build_num, test_id, capabilities, command_count, error_commands, error_repeat, username, access_key)

    def test_demo_site(self):
        build_count =  args.builds  # Change this to the number of builds you want to run
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(args.username)) as executor:
            for username, access_key in zip(args.username, args.access_key):
                for build_num in range(1, build_count + 1):
                    executor.submit(self._test_single_build, build_num, username, access_key)
            

if __name__ == "__main__":
    unittest.main(argv=[''])
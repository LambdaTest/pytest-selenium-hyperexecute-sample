import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

@pytest.fixture(scope='function')
def driver(request):
    
    options = ChromeOptions()
    
    # Browser configuration
    options.browser_version = "latest"
    options.platform_name = os.environ.get("TARGET_OS", "Windows 10")
    
    # LambdaTest specific options (Selenium 4 uses LT:Options capability)
    lt_options = {
        "build": "[Python] HyperTest demo using PyTest framework",
        "name": request.node.name,
        "video": True,
        "visual": True,
        "network": True,
        "console": True
    }
    options.set_capability("LT:Options", lt_options)
    
    username = os.environ.get("LT_USERNAME")
    access_key = os.environ.get("LT_ACCESS_KEY")
    
    selenium_endpoint = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"
    
    browser = webdriver.Remote(
        command_executor=selenium_endpoint,
        options=options
    )
    yield browser

    def fin():
        if request.node.rep_call.failed:
            browser.execute_script("lambda-status=failed")
        else:
            browser.execute_script("lambda-status=passed")
        browser.quit()

    request.addfinalizer(fin)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

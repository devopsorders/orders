"""
Environment for Behave Testing
"""
import os

from selenium import webdriver

from app import service

WAIT_SECONDS = 120
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')


def before_all(context):
    """ Executed once before all tests """

    # TODO PhantomJS is deprecated - should try to use headless chrome in the future, but too much work for this project
    # from selenium.webdriver.chrome.options import Options
    # options = Options()
    # options.headless = True
    # driver = webdriver.Chrome(options=options)  # chromedriver needs to be in PATH for this to work
    # context.driver = driver

    context.driver = webdriver.PhantomJS()
    # context.driver.manage().timeouts().pageLoadTimeout(WAIT_SECONDS, TimeUnit.SECONDS);
    # context.driver.manage().timeouts().setScriptTimeout(WAIT_SECONDS, TimeUnit.SECONDS);
    context.driver.implicitly_wait(WAIT_SECONDS)  # seconds
    context.driver.set_window_size(1120, 550)
    context.base_url = BASE_URL
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini"
    context.config.setup_logging()
    service.init_db()

from pathlib import Path
import configfile
import pytest
from selenium import webdriver
from ctreport_selenium.ctlistener import Session
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture(scope="module", autouse=True)
def driver_obj(request, browser, base_url, username, password):
    global driver
    if browser == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(GeckoDriverManager().install())
    elif browser == "ie":
        driver = webdriver.Ie(IEDriverManager().install())
    elif browser == "edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    Session.start(test_execution_name="Smoke Test - Orange HRM Web", path=str(Path(__file__).parent) + r"/reports/",
                  driver=driver,
                  config_file=str(Path(__file__).parent) + "/reportconfig.json")

    driver.maximize_window()
    driver.get(base_url)
    driver.implicitly_wait(10)
    from pages.loginpage import LoginPage
    login = LoginPage(driver)
    login.do_login(username, password)

    def quit_driver():
        Session.end()
        driver.quit()

    request.addfinalizer(quit_driver)
    return driver


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("-A")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("-B")


@pytest.fixture(scope="session")
def username(request):
    return request.config.getoption("-U")


@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("-P")


def pytest_addoption(parser):
    parser.addoption("-A", "--app_url",
                     dest="url",
                     default=configfile.base_url,
                     help="The url of the application")

    parser.addoption("-B", "--browser",
                     dest="browser",
                     default=configfile.browser,
                     help="Browser. Valid options are firefox, ie and chrome")

    parser.addoption("-U", "--username",
                     dest="username",
                     default=configfile.username,
                     help="Valid User Id")

    parser.addoption("-P", "--password",
                     dest="password",
                     default=configfile.password,
                     help="Valid Password")

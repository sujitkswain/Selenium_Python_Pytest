import time

from selenium.webdriver.common.by import By

from pages.basepage import BasePage


class LoginPage(BasePage):

    username_textfield = By.XPATH, "//input[@placeholder='Username']"
    password_textfield = By.XPATH, "//input[@placeholder='Password']"
    login_button = By.XPATH, "//button[@type='submit']"

    def do_login(self, uname, pword):
        element = self.wait_for_element(self.username_textfield, "visibility")
        element.send_keys(uname)
        self.type(self.password_textfield, pword)
        self.click(self.login_button)

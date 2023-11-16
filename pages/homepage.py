
from selenium.webdriver.common.by import By
from pages.basepage import BasePage


class HomePage(BasePage):

    dashboard = By.XPATH, "//h6[@class='oxd-text oxd-text--h6 oxd-topbar-header-breadcrumb-module'][text()='Dashboard']"
    profile = By.XPATH, "//li[contains(@class,'oxd-userdropdown')]"
    time_at_work = By.XPATH, "//P[@class='oxd-text oxd-text--p'][text()='Time at Work']"
    admin_menu = By.XPATH, "//SPAN[@class='oxd-text oxd-text--span oxd-main-menu-item--name'][text()='Admin']"
    admin_page = By.XPATH, "//h5[@class='oxd-text oxd-text--h5 oxd-table-filter-title'][text()='System Users']"

    def verify_dashboard(self):
        home_element = self.wait_for_element(self.dashboard, "visibility")
        return home_element.text

    def verify_profile(self):
        self.wait_for_element(self.profile, "visibility")

    def verify_time_at_work(self):
        self.wait_for_element(self.time_at_work, "visibility")

    def click_admin_menu(self):
        products_element = self.wait_for_element(self.admin_menu, "clickable")
        products_element.click()

    def verify_admin_page(self):
        home_element = self.wait_for_element(self.admin_page, "visibility")
        return home_element.text

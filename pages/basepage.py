from datetime import datetime
import os
from time import strptime
import pytesseract as pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configfile


class BasePage:

    driver = ""

    def __init__(self, d):
        self.driver = d

    def click(self, locator):
        # Why * is given, since, find_element needs two parameter then we have to pass the locator as *args
        element = self.driver.find_element(*locator)
        self.highlight(element)
        element.click()

    def type(self, locator, text):
        self.driver.find_element(*locator).send_keys(text)

    def get_text(self, locator):
        return self.driver.find_element(*locator).text

    def get_value_from_textbox(self, locator):
        return self.driver.find_element(*locator).get_attribute("value")

    def get_value_from_combobox(self, locator):
        element = self.driver.find_element(*locator)
        selected_value = element
        return selected_value.text

    def get_element_from_list(self, locator, text):
        if locator[0] == By.ID:
            return self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().resourceId("' + locator[
                    1] + '")).getChildByText(new UiSelector().className("col-md-11"),"' + text + '")'
            )
        elif locator[0] == By.CLASS_NAME:
            return self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().className("' + locator[
                    1] + '")).getChildByText(new UiSelector().className("col-md-11"),"' + text + '")'
            )

    def enter_text(self, locator, text):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    # This Method is not helpful for selecting dropdown,so not recommend to use it.
    # But kept it here as it is previously present(Comment By--Sujit Swain).
    def select_dropdown(self, locator, text):
        element = self.driver.find_element(*locator)
        return element

    # This Method is helpful for selecting value from the dropdown which have "Select" tag.
    def select_select_tag_dropdown(self, locator, text):
        sel = Select(self.driver.find_element(*locator))
        sel.select_by_visible_text(text)

    def go_to_year(self,year):
        while True:
            Y = int(self.driver.find_element_by_xpath("//span[@class='ui-datepicker-year']").text)
            if year < Y:
                self.driver.find_element_by_xpath("//span[text()='Prev']").click()
            elif year > Y:
                self.driver.find_element_by_xpath("//span[text()='Next']").click()
            else:
                break

    def go_to_month(self,month):
        while True:
            M = self.driver.find_element_by_xpath("//span[@class='ui-datepicker-month']").text[:3]
            M = strptime(M, '%b').tm_mon
            if month < M:
                self.driver.find_element_by_xpath("//span[text()='Prev']").click()
            elif month > M:
                self.driver.find_element_by_xpath("//span[text()='Next']").click()
            else:
                break

    def select_date(self,date):
        month = strptime(date.split('-')[1], '%b').tm_mon
        year = int(date.split('-')[2])
        day = date.split('-')[0]
        self.go_to_year(year)
        self.go_to_month(month)
        self.driver.find_element_by_xpath("//td[@data-handler='selectDay']/a[text()='" + day + "']").click()

    def get_element_by_text(self, locator, text):
        elements=self.driver.find_elements(*locator)
        for element in elements:
            if element.text == text:
                self.highlight(element)
                return element,len(elements)

    def wait_for_element(self, locator, condition):
        wait = WebDriverWait(self.driver, 10)
        if condition == "visibility":
            return wait.until(EC.visibility_of_element_located(locator))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable(locator))
        elif condition == "presence":
            return wait.until(EC.presence_of_element_located(locator))

    def wait_for_elements(self, locator, condition):
        wait = WebDriverWait(self.driver, 10)
        if condition == "visibility":
            return wait.until(EC.visibility_of_all_elements_located(locator))

    def _wait_for_element(self, locator, condition, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        if condition == "visibility":
            return wait.until(EC.visibility_of_element_located(locator))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable(locator))
        elif condition == "presence":
            return wait.until(EC.presence_of_element_located(locator))
        elif condition == "invisibility":
            return wait.until(EC.invisibility_of_element_located(locator))
        elif condition == "staleelementreferenceexception":
            wait = WebDriverWait(self.driver, timeout, ignored_exceptions=[StaleElementReferenceException])
            return wait.until(EC.presence_of_element_located(locator))

    def _wait_for_elements(self, locator, condition, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        if condition == "visibility":
            return wait.until(EC.visibility_of_any_elements_located(locator))
        elif condition == "presence":
            return wait.until(EC.presence_of_all_elements_located(locator))

    def highlight(self,element):
        # Highlight the element through execute_script function
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",element,"border: 2px solid red;")

    def accept_alert_window(self):
        alert_box = self.driver.switch_to.alert
        alert_box.accept()

    def get_element_by_index(self, locator, index):
        elements = self.driver.find_elements(*locator)
        return elements[index].text

    def get_elements(self, locator):
        elements = self.driver.find_elements(*locator)
        return elements

    def _get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def get_elements_text(self, locator):
        elements = self.driver.find_elements(*locator)
        return elements.text

    def take_screenshot(self, path=None):
            if path is None:
                os.makedirs("temp")
                path = r"temp/" + datetime.now().strftime("%d_%m_%y_%H%M%S") + ".png"
            self.driver.save_screenshot(path)
            return path

    def create_webelement_text_list(self,locator):
        target_list=self.wait_for_elements(locator,"visibility")
        '''
        i=0
        while i<listsize:
            element_list.append(target_list[i].text.strip())
            i+=1
        return  element_list
        '''
        '''
        for element in target_list:
            element_list.append(element.text.strip())
        return element_list
        '''
        element_list = [element.text.strip() for element in target_list]
        return element_list

    def get_text_by_tesseract(self, image_path):
        pytesseract.tesseract_cmd = configfile.tesseract_path
        im = Image.open(image_path)
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(4)
        im = im.convert('1')
        im.save(image_path)
        text = pytesseract.image_to_string(Image.open(image_path))
        return text

    def _click(self, locator):
        element = self.driver.find_element(*locator)
        element.click()

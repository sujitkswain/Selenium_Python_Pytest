# Selenium_Python_Pytest
This is the project for Selenium, Python, and Pytest. ctreport-selenium is used for reporting. Basically, it is a hybrid framework. POM and data-driven testing have been followed.

Dependencies:
----------------
-> Refer it in requirement.txt

Folder/Package Structure:
-------------------------
->pages - POM (Page Object Model)- Design Pattern
-------------------------------------------------
  BasePage class, hold all the selenium interaction like click(locator), enter_text(locator,text)
  Page classes like HomePage, LoginPage 
  Page objects -> By locators like By.ID, "signin_button"
  Page actions -> def click_login_button():
  has to inherit the BasePage
  
->testdata
-----------
  Excel file that holds the test data
  read_from_excel.py - responsible for reading data from the Excel (xlrd)
  getdata.py - responsible for reading data from the Excel (openpyxl)
  
->reports
----------
  html reports (ctreport-selenium)

->tests
---------
  pytest test methods
  
Root Directory/Project Directory
  regressionsuite.ini(To run multiple files at a time)
  conftest.py (For the setup and tear down methods and also driver initialization and invoking browser and also login to app)
  README.md
  requirements.txt (All the dependencies are available)
  configfile.py(Base Url and which browser you want to run should be present in this file)

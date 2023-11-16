import time

import pytest
from ctreport_selenium.ctlistener import Test
from pages.homepage import HomePage
from testdata.getdata import get_data


class TestHomePageVerification:
    driver = None
    test = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setupclass(cls, driver_obj):
        TestHomePageVerification.driver = driver_obj

    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("data", get_data("Test Data.xlsx", "Test Data"))
    def test_home_page_verification(self, data):
        self.test = Test("Home Page and Admin Page Verification Test for Orange HRM",
                         description="Home Page and Navigate to Dashboard Page Verification Test and also"
                                     "Admin Page verification Test")

        self.test.log("Home Page and Admin Page Verification Test Started")

        home_page = HomePage(self.driver)

        actual_name = home_page.verify_dashboard()

        expected_name = data["Dashboard Name"]

        self.test.assert_are_equal(actual_name, expected_name, description="Successfully Navigated to Dashboard Page",
                                   onfail_screenshot=False)
        home_page.verify_profile()
        self.test.log("Profile field Verification Success")
        home_page.verify_time_at_work()
        self.test.log("Time_at_work field Verification Success")
        home_page.click_admin_menu()
        self.test.log("Admin Menu clicked Success")
        actual_name = home_page.verify_admin_page()
        expected_name = data["Admin Page"]
        self.test.assert_are_equal(actual_name, expected_name, description="Successfully Navigated to Admin Page",
                                   onfail_screenshot=False)
        time.sleep(1)
        self.test.log("Home Page and Admin Page Verification Test Ended")

    def teardown_method(self, method):
        self.test.finish()

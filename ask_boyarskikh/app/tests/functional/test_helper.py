#!/usr/bin/python3
from django.test import LiveServerTestCase
from selenium.webdriver import Chrome
import os


class ApplicationLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.set_window_size(1024, 960)

    def setUp(self):
        super().setUp()
        self.driver = self.__class__.driver

    def tearDown(self):
        result = self.defaultTestResult()
        self._feedErrorsToResult(result, self._outcome.errors)
        error = self._list2reason(result.errors)
        failure = self._list2reason(result.failures)
        ok = not error and not failure

        if not ok:
            screenshot_path = 'screenshots/' + self.id() + '.png'
            self.driver.save_screenshot(screenshot_path)
            print('\nScreenshot saved here: ' + os.path.realpath(screenshot_path))
        super().tearDown()

    def _list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

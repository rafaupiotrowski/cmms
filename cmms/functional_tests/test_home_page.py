from django.contrib.staticfiles.testing import LiveServerTestCase

import sys

from selenium import webdriver

class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        print(self.live_server_url, file=sys.stderr)


    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        super().tearDownClass()

    #User enter home site and see cmms in title
    def test_Django_in_title(self):
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)
        print('łącze do: ', self.live_server_url, file=sys.stderr)
        self.browser.implicitly_wait(100)
        self.assertIn('cmms', self.browser.title)
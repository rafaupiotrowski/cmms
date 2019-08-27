from django.contrib.staticfiles.testing import LiveServerTestCase
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from breakdowns.models import Machine


class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        super().tearDownClass()

    # User enter home site and see cmms in title
    def test_cmms_in_title(self):
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)
        print('łącze do: ', self.live_server_url, file=sys.stderr)
        self.assertIn('Cmms', self.browser.title)

    # In home page breakdown can be registered...
    def test_register_breakdown_on_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Register breakdown', self.browser.page_source)

    # ...Machine can be chosen from dropdown menu...
    def test_machine_dropdown_list_on_home_page(self):
        Machine.objects.create(name="Machine 1")
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(10)
        machines_list = self.browser.find_element_by_tag_name("select")
        all_options = machines_list.find_elements_by_tag_name("option")
        all_options = [option.get_attribute("text") for option in all_options]
        self.assertIn('Machine 1', all_options)

    # ...and breakdown time can be picked. User enter start and end time...
    def test_datetime_picker_for_breakdown_time_available(self):
        self.browser.get(self.live_server_url)
        breakdown_start = self.browser.find_element_by_id('id_start_time')
        breakdown_start.send_keys('2009-10-25 14:30')
        breakdown_end = self.browser.find_element_by_id('id_end_time')
        breakdown_end.send_keys('2009-10-26 14:30')

    # and press 'save' button
        self.browser.find_element_by_id('save_breakdown').click()

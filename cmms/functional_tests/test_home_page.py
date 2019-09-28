from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from breakdowns.models import Machine


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.browser = webdriver.Chrome()
        Machine.objects.create(name="Machine 1")

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        super().tearDownClass()


class BreakdownRegistrationTest(FunctionalTest):

    def test_breakdown_can_be_saved(self):
        # User enter home site and see cmms in title
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)
        self.assertIn('Cmms', self.browser.title)

        # In home page user is encouraged to register breakdown...
        self.assertIn('Register breakdown', self.browser.page_source)

        # ...Machine can be chosen from dropdown menu...
        machines_list = self.browser.find_element_by_tag_name("select")
        all_options = machines_list.find_elements_by_tag_name("option")
        all_options = [option.get_attribute("text") for option in all_options]
        self.assertIn('Machine 1', all_options)

        # user choose Machine 1 option
        select = Select(self.browser.find_element_by_id('id_machine'))
        select.select_by_visible_text('Machine 1')

    # ...and breakdown time can be picked. User enter start and end time...
        breakdown_start = self.browser.find_element_by_id('id_start_time')
        breakdown_start.send_keys('2009-10-25 14:30')
        breakdown_end = self.browser.find_element_by_id('id_end_time')
        breakdown_end.send_keys('2009-10-26 14:30')

    # and enter short description of breakdown
        description = self.browser.find_element_by_id(
            'id_breakdown_description')
        description.send_keys('Main motor failure')

    # and press 'save' button
        self.browser.find_element_by_id('save_breakdown').click()

    # message about succesful breakdown save is displayed
        list_items = self.browser.find_elements_by_tag_name('li')
        messages = [li.text for li in list_items]
        self.browser.implicitly_wait(10)
        self.assertIn('Breakdown successfully saved.', messages)

    # user choose 'All breakdowns' option from sidebar
        all_breakdowns = self.browser.find_element_by_link_text(
                                                        'All breakdowns')
        all_breakdowns.click()

    # new page contains registered breakdowns
        all_breakdowns_page_content = self.browser.find_element_by_id('content')
        self.assertIn("Registered breakdowns", all_breakdowns_page_content.text)

    # table with all breakdowns contains just created breakdown
        all_breakdowns_table = self.browser.find_element_by_id('all_breakdowns_table')
        self.assertIn('Main motor failure', all_breakdowns_table.text)

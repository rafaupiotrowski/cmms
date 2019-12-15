from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from breakdowns.models import Machine, Breakdown


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.browser = webdriver.Chrome()
        self.Machine_1 = Machine.objects.create(name="Machine 1")

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
        list_items = self.browser.find_elements_by_id('messages')
        messages = [li.text for li in list_items]
        self.browser.implicitly_wait(10)
        self.assertIn('Breakdown successfully saved.', messages)

    # user choose 'All breakdowns' option from sidebar
        all_breakdowns = self.browser.find_element_by_link_text(
                                                        'All breakdowns')
        all_breakdowns.click()

    # table with all breakdowns contains just created breakdown
        all_breakdowns_table = self.browser.find_element_by_id(
            'all_breakdowns_table')
        self.assertIn('Main motor failure', all_breakdowns_table.text)


class FilteringBreakdownsTest(FunctionalTest):
    def create_breakdown(
            self,
            machine=None,
            start_time='2009-10-25 14:30',
            end_time='2009-10-25 15:30',
            breakdown_description='test_description'):
        if not machine:
            machine = self.Machine_1
        start_time = timezone.make_aware(parse_datetime(start_time))
        end_time = timezone.make_aware(parse_datetime(end_time))
        Breakdown.objects.create(
            machine=machine, start_time=start_time,
            end_time=end_time, breakdown_description=breakdown_description)

    def testFiltering(self):
        print('test filtering first line, all machines: ', Machine.objects.all())
        self.create_breakdown(breakdown_description='breakdown_1')
        self.create_breakdown(breakdown_description='breakdown_2')

        # user enter home page and choose all_breakdowns tab
        self.browser.get(self.live_server_url)
        all_breakdowns = self.browser.find_element_by_link_text(
                                                        'All breakdowns')
        all_breakdowns.click()

        # there is a form for filtering breakdowns
        form = self.browser.find_element_by_class_name('form-group')

        # user enter breakdown description and click search button
        breakdown_description_field = form.find_element_by_id(
                                                    'id_breakdown_description')
        breakdown_description_field.send_keys('breakdown_1')
        search_button = form.find_element_by_id('submit_form')
        search_button.click()

        # in table below appear one breakdown with description given above
        breakdowns = self.browser.find_element_by_id(
                                                        'all_breakdowns_table')
        breakdowns_headers = [th.text for th in breakdowns.find_elements_by_css_selector('th')]
        breakdowns_data = [td.text for td in breakdowns.find_elements_by_css_selector('td')]

        self.assertEqual(len(breakdowns_headers), len(breakdowns_data))

        # user want to filter other breakdowns with 'breakdown' in description
        form = self.browser.find_element_by_class_name('form-group')

        breakdown_description_field = form.find_element_by_id(
                                                    'id_breakdown_description')
        breakdown_description_field.clear()
        breakdown_description_field.send_keys('breakdown')
        search_button = form.find_element_by_id('submit_form')
        search_button.click()

        breakdowns = self.browser.find_element_by_id(
                                                    'all_breakdowns_table')
        breakdowns_data = [td.text for td in breakdowns.find_elements_by_css_selector('td')]
        self.assertEqual(len(breakdowns_data), 10)

    def test_breakdown_details_view(self):
        breakdown_details_machine = Machine.objects.create(name='breakdown_details_machine')
        self.create_breakdown(
                            machine=breakdown_details_machine,
                            breakdown_description='breakdown_details_test')

        self.browser.get(self.live_server_url)
        all_breakdowns = self.browser.find_element_by_link_text(
                                                                'All breakdowns')
        all_breakdowns.click()

        # user want to see breakdowns details, so click on details button
        details_button = self.browser.find_element_by_id('details')
        details_button.click()

        # breakdown description is displayed on page
        page_content = self.browser.page_source
        self.assertIn('breakdown_details_test', page_content)

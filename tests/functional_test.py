#!/bin/env python

import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        # Checkout the homepage
        self.browser.get("http://localhost:8000")

        # check the title and header is t-do lists
        self.assertIn("To-Do lists", self.browser.title)
        header_test = self.browser.find_element(By.TAG_NAME, "h1")

        self.assertIn("To-Do lists", header_test.text)

        # she is invited to enter a to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # she types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)
        self.send_new_item("Buy peacock feathers")
        self.check_for_row_in_list("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.send_new_item("Use peacock feathers to make a fly")
        self.check_for_row_in_list("1: Buy peacock feathers")
        self.check_for_row_in_list("2: Use peacock feathers to make a fly")

        # Edith wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for her -- there is some explanatory text to that effect.
        self.fail("Finish the test!")

    def check_for_row_in_list(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def send_new_item(self, new_item):
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys(new_item)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()

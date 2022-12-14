from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from unittest import TestCase, main

import string
import random
import time


def generate_text():
    """Generate and return random string with 250-400 characters."""
    text = ''.join(random.choices(string.ascii_letters, k=random.randrange(250, 401)))
    return text

class TestTranslateService(TestCase):
    """Test case for traslation service."""
    
    def setUp(self):
        """Initialization of webdriver."""
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def tearDown(self):
        """Cleanup method."""
        self.driver.close()

    def test_expected_price_and_time_presence(self):
        """Test expected price and realization time precence."""
        driver = self.driver

        url = 'https://turbotlumaczenia.pl/'
        driver.get(url)

        order_translation_button = driver.find_element(By.ID, 'clouds').find_element(By.TAG_NAME, 'a')
        order_translation_button.click()

        translate_to_form = driver.find_element(By.ID, 'dropdown-col-to1')
        translate_to_form.click()
        translate_to_dropwdown = driver.find_element(By.ID, 'target1_lang_dropdown')
        translate_to_en = translate_to_dropwdown.find_element(By.ID, 'Row_1en')
        translate_to_de = translate_to_dropwdown.find_element(By.ID, 'Row_16de')
        translate_to_en.click()
        translate_to_de.click()
        translate_to_form.click()

        proofreading = driver.find_element(By.ID, 'proofreading')
        proofreading.click()

        text_area = driver.find_element(By.ID, 'content')
        text_area.click()
        text_area.send_keys(generate_text())

        time.sleep(3)
        try:
            realization_time = driver.find_element(By.XPATH, "//span[contains(text(), 'godz')]")
            expected_price = driver.find_element(By.XPATH, "//span[contains(text(), 'z??')]")
        except NoSuchElementException:
            realization_time = None
            expected_price = None
        
        self.assertIsNotNone(realization_time)
        self.assertIsNotNone(expected_price)

if __name__ == '__main__':
    main()
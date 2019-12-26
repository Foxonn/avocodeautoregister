from nickname_generator import generate
import passgen
import os
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pyperclip
import traceback


class AvocodeRA:
    browser = ''

    SILENT_START = 'false'
    WRITE_TO_FILE = 'true'
    TIMER_WAIT_CONFIRM = 60
    MAIL_SERVICE = 'emailfake'
    ACESS_FILENAME = 'access.txt'
    PATH_TO_SAVE = ''
    WEBDRIVER_PATH = ''
    LOGS_PATH = ''

    def __init__(self):
        print("Notify: Begin create new account")
        self.__name = ''
        self.__email = ''
        self.__password = ''

    def set_option(self):
        print("Notify: Set options")
        # Установка параметров загрузки драйвера

        chrome_options = webdriver.ChromeOptions()

        prefs = {"profile.managed_default_content_settings.images": 2}

        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("prefs", prefs)

        if self.SILENT_START == 'true':
            chrome_options.add_argument('--window-position=0,-2500')
            chrome_options.add_argument('--window-size=0,0')

        if self.WEBDRIVER_PATH:
            self.browser = webdriver.Chrome(self.WEBDRIVER_PATH, options=chrome_options)
        else:
            self.browser = webdriver.Chrome('chromedriver.exe', options=chrome_options)

    def get_email(self):
        print("Notify: {0} loading waiting".format(self.MAIL_SERVICE.capitalize()))

        if self.MAIL_SERVICE == 'emailfake':
            self.browser.get('https://emailfake.com')

            WebDriverWait(self.browser, 15).until(ec.presence_of_element_located((By.TAG_NAME, 'body')),
                                                  'Error: Email service "emailfake" not loading !')

            print("Notify: {0} loaded".format(self.MAIL_SERVICE.capitalize()))

            WebDriverWait(self.browser, 15).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#email_ch_text')),
                                                  'Error: Field Email address not found !')

            return self.browser.find_element_by_id('email_ch_text').get_attribute('textContent')

    def get_avocode(self):
        print("Notify: Avocode loading waiting")

        WebDriverWait(self.browser, 15).until(
            ec.presence_of_element_located((By.TAG_NAME, 'body')), 'Error: Avocode page not loaded !')
        self.browser.execute_script("window.open('https://avocode.com/signup/','_blank');")

        print("Notify: Avocode loaded")

    def sign_in_avocode(self):
        print("Notify: Begin registration new account")

        self.__name = generate('en')
        self.__email = self.get_email()
        self.__password = passgen.passgen()

        self.browser.switch_to.window(self.browser.window_handles[1])

        # Wait loading form
        WebDriverWait(self.browser, 15).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'form#registrationForm')), "Error: Form not found !")

        # check is not continue registration
        WebDriverWait(self.browser, 15).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'label[class^=Agree]')),
            "Error: Is continue registration !")

        # Form filling
        self.browser.find_element_by_id('name').send_keys(self.__name)
        self.browser.find_element_by_id('email').send_keys(self.__email)
        self.browser.find_element_by_id('password').send_keys(self.__password)
        Select(self.browser.find_element_by_id('role')).select_by_index(2)
        self.browser.find_element_by_id('team').send_keys(self.__name)
        self.browser.find_element_by_css_selector('label[class^=Agree]').click()
        self.browser.find_element_by_id('registrationForm').submit()

        WebDriverWait(self.browser, 30).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'button[class^=DeclineButton]')), "Error: Form submission failed !")

        self.browser.close()

    def confirm_registration(self):
        print("Notify: Beginning confirm registration")

        self.browser.switch_to.window(self.browser.window_handles[0])

        if self.MAIL_SERVICE == 'emailfake':
            WebDriverWait(self.browser, int(self.TIMER_WAIT_CONFIRM)).until(
                ec.presence_of_element_located(
                    (By.PARTIAL_LINK_TEXT, 'https://avocode.com/confirm-email')),
                "Error: Link verification not found !")

            print("Notify: Link verification found !")

        WebDriverWait(self.browser, 20).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'td>a[href^="https://avocode.com/confirm-email"]')),
            "Error: Verify not found !")

        print("Notify: Verify found !")

        self.browser.find_element_by_css_selector('td>a[href^="https://avocode.com/confirm-email"]').click()

        time.sleep(3)

        self.browser.switch_to.window(self.browser.window_handles[1])

        WebDriverWait(self.browser, 40).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[class*="VerificationScreen_"] > button[class*="buttonStyle"]')),
            "Error: Verify not confirm !")

        self.browser.find_element_by_css_selector(
            'div[class*="VerificationScreen_"] > button[class*="buttonStyle"]').click()

        WebDriverWait(self.browser, 40).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'button[data-ui="save-form__save-button"]')),
            'Error: Pressed not button confirm !')

        print("Notify: Registration is confirmed")

    def save_to_buffer(self):

        access = self.__email + " " + self.__password

        pyperclip.copy(self.__email)
        pyperclip.copy(self.__password)
        pyperclip.copy(access)
        pyperclip.paste()

        print("Success: Access sent to clipboard")

    def save_access(self, file_name=None):

        if file_name is None:
            file_name = self.ACESS_FILENAME

        if self.WRITE_TO_FILE == 'true':
            if self.PATH_TO_SAVE:
                file_output = self.PATH_TO_SAVE + file_name
            else:
                file_output = file_name

            access = {"name": self.__name, "email": self.__email, "password": self.__password}

            if os.path.exists(file_output):
                with open(file_output, 'a') as outfile:
                    outfile.write(',\n' + str(access))
            else:
                with open(file_output, 'w') as outfile:
                    outfile.write(str(access))

            print("Success: Accesses are written to file")


driver = AvocodeRA()

if len(sys.argv) > 1:

    for arg in sys.argv:
        result = re.search(r'^(.*)=(.*)$', str(arg))

        if result is not None:
            if result.group(1) in 'mail':
                driver.MAIL_SERVICE = result.group(2)

            if result.group(1) in 'duration':
                driver.TIMER_WAIT_CONFIRM = result.group(2)

            if result.group(1) in 'hide':
                driver.SILENT_START = result.group(2)

            if result.group(1) in 'path':
                driver.PATH_TO_SAVE = result.group(2)

            if result.group(1) in 'wfile':
                driver.WRITE_TO_FILE = result.group(2)

            if result.group(1) in 'wdpath':
                driver.WEBDRIVER_PATH = result.group(2)

if __name__ == '__main__':
    try:
        driver.set_option()
        driver.get_avocode()
        driver.sign_in_avocode()
        driver.confirm_registration()
        driver.save_access()
        driver.save_to_buffer()
    except Exception as err:
        # driver.save_access('fail.txt')
        print("Error: " + str(err) + traceback.format_exc())
    finally:
        print("Notify: Exit")
# driver.browser.get_screenshot_as_file('screenshots/last-error.png')
# driver.browser.quit()

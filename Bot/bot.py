from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class Bot:
    def __init__(self, fullscreen=True):
        self.driver = webdriver.Chrome('C:/Users/Lenovo/Documents/projects/BotCookieClicker/drivers/chromedriver.exe')
        self.cookies = ""
        self.mission()

    def mission(self):
        raise NotImplementedError()

    def send_keys(self, xpath, keys, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(keys)

    def click_on_element(self, xpath, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def get_text_from_element(self, xpath, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).text

    def find_element_by_xpath(self, xpath, timeout=10, false_on_not_found=False):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException as e:
            if false_on_not_found:
                return False
            else:
                raise e

    def find_elements_by_xpath(self, xpath, timeout=10, false_on_not_found=False):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException as e:
            if false_on_not_found:
                return False
            else:
                raise e

    def get(self, url):
        self.driver.get(url)

    def move_to_element_and_click(self, xpath):
        # TODO: Improves method
        element = self.driver.find_element(By.XPATH, xpath)
        action = ActionChains(self.driver)
        try:
            action.move_to_element(element).perform()
            element = self.driver.find_element(By.XPATH, xpath)
            element.click()
            return True
        except Exception as e:
            # TODO: treat exceptions
            return False

    @staticmethod
    def parse_cookies(selenium_cookies):
        cookies = {}
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])
        return cookie_string

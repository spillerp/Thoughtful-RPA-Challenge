from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging


class CustomSelenium:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)

    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options

    def set_webdriver(self):
        options = self.set_chrome_options()
        self.driver = webdriver.Chrome(options)
        print("WebDriver initialized successfully.")

    def open_url(self, url: str, screenshot: str = None):
        self.driver.get(url)
        if screenshot:
            self.driver.get_screenshot_as_file(screenshot)

    def wait_for_element(self, xpath: str):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def get_element(self, xpath: str) -> WebElement:
        self.wait_for_element(xpath)
        return self.driver.find_element(By.XPATH, xpath)

    def get_element_text(self, xpath: str) -> str:
        self.wait_for_element(xpath)
        element = self.driver.find_element(By.XPATH, xpath)
        return element.text

    def click_button(self, xpath: str):
        self.wait_for_element(xpath)
        button = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].click()", button)

    def input_text(self, xpath: str, text: str, enter: bool = False):
        self.wait_for_element(xpath)
        input_box = self.driver.find_element(By.XPATH, xpath)
        for char in text:
            self.driver.execute_script(
                "arguments[0].value += arguments[1];", input_box, char
            )
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                input_box
            )
            time.sleep(0.5)
        if enter:
            self.driver.execute_script(
                """arguments[0].dispatchEvent(new KeyboardEvent('keydown', 
                { key: 'Enter', keyCode: 13, which: 13 }));""",
                input_box
            )
            self.driver.execute_script(
                """arguments[0].dispatchEvent(new KeyboardEvent('keyup', 
                { key: 'Enter', keyCode: 13, which: 13 }));""",
                input_box
            )
            self.driver.execute_script(
                """arguments[0].dispatchEvent(new KeyboardEvent('keypress', 
                { key: 'Enter', keyCode: 13, which: 13 }));""",
                input_box
            )

    def count_childs(self, parent_xpath: str):
        self.wait_for_element(parent_xpath)
        parent_element = self.driver.find_element(By.XPATH, parent_xpath)
        child_elements = parent_element.find_elements(By.XPATH, './div')
        return len(child_elements)

    def get_info_from_childs(self, parent_xpath: str):
        self.wait_for_element(parent_xpath)
        parent_element = self.driver.find_element(By.XPATH, parent_xpath)
        child_elements = parent_element.find_elements(By.XPATH, './div')
        results = []
        for i, child in enumerate(child_elements):
            data = self.process_child_element(child, i + 1)
            results.append(data)
        return results

    def process_child_element(self, child_element: WebElement, index: int):
        data = {'index': index}
        data['h2_text'] = self.get_element_text(
            child_element, './/div[@class="h2"]'
        )
        data['p_text'] = self.get_element_text(child_element, './/p')
        data['author'] = self.get_element_text(
            child_element, (
                "//div[@id='resultList']//a[contains(@class, 'flexible-link') "
                "and contains(@class, 'internal') and contains(@class, "
                "'v-byline-author-name')]"
            )
        )
        data['img_srcs'] = self.get_element_attributes(
            child_element, './/img', 'src'
        )
        return data

    def get_element_text(self, parent: WebElement, xpath: str) -> str:
        try:
            element = parent.find_element(By.XPATH, xpath)
            return element.get_attribute('innerHTML')
        except:
            return ''

    def get_element_attributes(self, parent: WebElement, xpath: str, attribute: str):
        elements = parent.find_elements(By.XPATH, xpath)
        for element in elements:
            attr_value = element.get_attribute(attribute)
            if attr_value:
                return attr_value
        return ''

    def driver_quit(self):
        if self.driver:
            self.driver.quit()

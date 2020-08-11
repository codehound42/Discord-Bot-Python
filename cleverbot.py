from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import asyncio


class Cleverbot:
    
    def __init__(self):
        # Init selenium options/arguments
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.browser = webdriver.Firefox(options=self.opts)
        self.url = "https://www.cleverbot.com"


    async def init_connection(self):
        print("Initialising connection...")
        self.browser.get(self.url)
        self.browser.find_element_by_id('noteb').click()
        self.elem = self.browser.find_element_by_class_name("stimulus")


    async def close(self):
        print("Closing connection...")
        self.browser.quit()


    async def get_response(self, message):
        # Send message
        self.elem.send_keys(message + Keys.RETURN)
        await asyncio.sleep(3)

        # Get response
        line = self.browser.find_element_by_id("line1")
        response = line.text
        return response

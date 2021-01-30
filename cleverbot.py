from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import asyncio


class Cleverbot:

    def __init__(self):
        # Init selenium options/arguments
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.browser = webdriver.Firefox(options=self.opts, service_log_path="logs/geckodriver.log")
        self.url = "https://www.cleverbot.com"


    async def init_connection(self):
        print("Initialising connection...")
        self.browser.get(self.url)
        self.browser.find_element_by_id('noteb').click()
        self.elem = self.browser.find_element_by_class_name("stimulus")


    async def close(self):
        print("Closing connection...")
        self.browser.quit()


    async def get_response(self, message, is_retry_attempt=False):
        try:
            # Send discord message to cleverbot
            self.elem.send_keys(message + Keys.RETURN)

            # ### Get response ###
            # Since the cleverbot website returns the response letter by letter,
            # we loop to ensure we get the entire response message before returning
            waiting_time_quota = 15 # Maximum waiting time for response set to 15 seconds
            response_before = ""
            response_now = ""
            has_received_some_response = False
            is_still_receiving_response = False
            is_waiting_time_up = False
            while (not has_received_some_response or is_still_receiving_response) and not is_waiting_time_up:
                response_before = response_now
                response_now = self.browser.find_element_by_id("line1").text
                has_received_some_response = response_now.strip() != ""
                is_still_receiving_response = response_now != response_before
                is_waiting_time_up = waiting_time_quota <= 0
                waiting_time_quota -= 1
                await asyncio.sleep(1)

            return response_now
        except StaleElementReferenceException:
            if is_retry_attempt:
                return ""

            # Ensure form is focused properly after sudden page refreshes
            # The cleverbot website seems to refresh the page after some message exchanges and changes the url by appending /? followed by a low int
            await asyncio.sleep(3)
            self.elem = self.browser.find_element_by_class_name("stimulus")
            return await self.get_response(message, is_retry_attempt=True)

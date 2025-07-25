import os
from datetime import datetime
from django.test import LiveServerTestCase
from selenium import webdriver


class TestBase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.__init_browser()
        self.browser.implicitly_wait(3)

        if test_server := os.environ.get("APP_URL"):
            self.live_server_url = "http://" + test_server

        self.browser.get(self.live_server_url)

        self.article = {
            "title": "Test Article",
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "content": "Test Content"
        }

        self.about_me = {
            "title": "About Me",
            "content": "Something about me"
        }

        self.test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]

    def tearDown(self) -> None:
        self.browser.close()
    
    def __init_browser(self) -> webdriver.Remote:
        """Initialize webdriver object for Remote driver.

        Returns
        -------
        webdriver.Remote
            Instance of Remote webdriver.
        """
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        selenium_url = os.environ.get("SELENIUM_REMOTE_URL")

        return webdriver.Remote(
            command_executor=selenium_url,
            options=firefox_options,
        )

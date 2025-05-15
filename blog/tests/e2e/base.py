from datetime import datetime
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestBase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.__init_browser()
        self.browser.implicitly_wait(3)
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
    
    def __init_browser(self) -> webdriver.Chrome:
        """Initialize webdriver object for Chrome.

        Returns
        -------
        webdriver.Chrome
            Instance of Chrome webdriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

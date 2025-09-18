import os
from datetime import datetime
from django.test import LiveServerTestCase
from selenium.webdriver import DesiredCapabilities
from testcontainers.selenium import BrowserWebDriverContainer

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestBase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = int(os.environ.get("TEST_PORT", cls.port))
        cls.live_server_uri = "http://web:{}".format(cls.port)
        super(TestBase, cls).setUpClass()

    def setUp(self) -> None:
        self.browser_container = BrowserWebDriverContainer(
            DesiredCapabilities.CHROME
        )
        self.browser_container.start()

        self.browser = self.browser_container.get_driver()
        self.browser.implicitly_wait(3)

        server_host = os.environ.get("TEST_HOST", "host.docker.internal")
        self.live_server_url = f'http://{server_host}:{self.port}/'    
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
        self.browser_container.stop()

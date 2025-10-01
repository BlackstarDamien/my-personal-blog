import os
from datetime import datetime
from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright


class TestBase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        
        super(TestBase, cls).setUpClass()

    def setUp(self) -> None:
        self.page = self.browser.new_page()
        self.page.goto(self.live_server_url)

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
            {"title": "Test Article 1", "content": "Test Article 1", "slug": "test-article-1"},
            {"title": "Test Article 2", "content": "Test Article 2", "slug": "test-article-2"},
            {"title": "Test Article 3", "content": "Test Article 3", "slug": "test-article-3"}
        ]

    def tearDown(self) -> None:
        self.page.close()
        super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

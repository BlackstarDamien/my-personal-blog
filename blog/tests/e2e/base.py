from datetime import datetime
from typing import Dict
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from blog.models import AboutMe, Article


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

        self.admin = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "adm1n"
        }

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

    def create_dummy_articles(self):
        """Creates dummy articles.
        """
        test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]
        for article in test_articles:
            self.create_dummy_article(article)

    def create_dummy_article(self, article: Dict[str, str]) -> Article:
        """Create dummy article and returns Article's title.

        Parameters
        ----------
        article : Dict[str, str]
            Data used to initialize Article page's model.

        Returns
        -------
        Article
            Instance of created article.
        """
        return Article.objects.create(**article)

    def create_dummy_about_me_page(self, data: Dict[str, str]) -> AboutMe:
        """Create dummy About Me page.

        Parameters
        ----------
        data : Dict[str, str]
            Data used to initialize About Me page's model.

        Returns
        -------
        AboutMe
            Instance of AboutMe model.
        """
        return AboutMe.objects.create(**data)

    def create_dummy_admin_user(self):
        """Create Admin user for testing purposes.
        """
        User.objects.create_superuser(**self.admin)
    
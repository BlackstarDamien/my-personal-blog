from typing import Dict, Tuple
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from blog.models import Article

PAGES_TITLES = {
    "admin": lambda name: f"Select {name.lower()} to change | Django site admin",
    "edit_article": lambda name: f"{name} | Change article | Django site admin",
}


class TestBase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.__init_browser()
        self.browser.implicitly_wait(3)

        self.article = {
            "title": "Test Article",
            "content": "Test Content"
        }

    def tearDown(self) -> None:
        self.browser.close()
    
    def __init_browser(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

    def given_a_main_page(self):
        """Goes to blog main page.
        """
        self.browser.get(self.live_server_url)

    def when_click_link(self, link_text: str):
        """Clicks on given link name.

        Args:
            link_text (str): Name of link to click.
        """
        self.browser.find_element(By.LINK_TEXT, link_text).click()
    
    def then_i_am_on_the_page(self, page_name: str, element_name: str):
        expected_name = PAGES_TITLES[page_name](element_name)
        self.assertEqual(expected_name, self.browser.title)

    def create_dummy_article(self, article: Dict[str, str]) -> Tuple[int, str]:
        """Create dummy article and returns Article's title.

        Returns:
            Tuple[int, str]: Id and title of created article.
        """
        article = Article.objects.create(**article)
        return article.id, article.title
from datetime import datetime
from blog.models import Article
from django.test import LiveServerTestCase
from django.template.defaultfilters import slugify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class TestArticlePage(LiveServerTestCase):
    def setUp(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.implicitly_wait(3)

        self.article = {
            "title": "Test Article",
            "content": "Test Content"
        }

    def tearDown(self) -> None:
        self.browser.close()
    
    def test_properly_displays_article_page(self):
        """Tests that article page is displayed correctly
        with following sections:
        - Title
        - Publish date
        - Content
        """
        self.create_dummy_article(self.article)
        
        self.given_a_main_page()
        self.when_click_link(self.article["title"])
        self.then_i_can_see_article_page(self.article["title"])

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
    
    def then_i_can_see_article_page(self, page_name: str):
        """Checks if article is displayed properly.
        """
        expected_url = f"{self.live_server_url}/articles/{slugify(page_name)}"
        self.assertEqual(expected_url, self.browser.current_url)

        title = self.browser.find_element(By.CSS_SELECTOR, ".article-title")
        publish_date = self.browser.find_element(By.CSS_SELECTOR, ".article-pub-date")
        content = self.browser.find_element(By.CSS_SELECTOR, ".article-content")
        
        current_article = {
            "title": title.text,
            "publish_date": publish_date.text,
            "content": content.text
        }
        expected_article = {
            "title": self.article["title"],
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "content": self.article["content"]
        }
        self.assertDictEqual(current_article, expected_article)

    def create_dummy_article(self, article):
        """Creates dummy article.
        """
        Article.objects.create(**article)

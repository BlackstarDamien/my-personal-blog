from datetime import datetime
from django.template.defaultfilters import slugify
from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase


class TestArticlePage(TestBase):    
    def test_displays_article_page(self):
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

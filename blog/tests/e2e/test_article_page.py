from datetime import datetime
from django.template.defaultfilters import slugify
from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase


class TestArticlePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.current_article = self.create_dummy_article(self.article)
        self.create_dummy_about_me_page(self.about_me)
        
    def test_displays_article_page(self):
        """Tests that article page is displayed correctly
        with following sections:
        - Title
        - Publish date
        - Content
        """
        self.given_a_page("Main")
        self.when_click_link(self.article["title"])
        self.then_i_can_see_article_page(self.article["title"])
    
    def test_clicking_on_logo_redirects_to_main_page(self):
        """Tests that clicking on blog's name redirect user
        to the main page.
        """
        self.given_a_page("Article", self.current_article.slug)
        self.when_click_link("My Personal Blog")
        self.then_i_am_on_the_main_page()
    
    def test_clicking_on_posts_tab_redirects_to_main_page(self):
        """Tests that clicking on 'Posts' tab in navbar redirect user
        to the main page.
        """
        self.given_a_page("Article", self.current_article.slug)
        self.when_click_link("Posts")
        self.then_i_am_on_the_main_page()
    
    def test_clicking_on_about_me_tab_redirects_to_about_me_page(self):
        """Tests that clicking on 'About Me' tab in navbar redirect user
        to the About Me page.
        """
        self.given_a_page("Article", self.current_article.slug)
        self.when_click_link("About Me")
        self.then_i_can_see_about_me_page()
    
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

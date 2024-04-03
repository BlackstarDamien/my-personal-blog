from datetime import datetime
from blog.tests.e2e.base import TestBase

from .pages.article_page import ArticlePage
from .pages.main_page import MainPage
from .pages.admin_login_page import AdminLoginPage
from .pages.admin_page import AdminArticlePage


class TestArticles(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_create_article(self):
        """Tests that it's possible to add an article via admin panel.
        """
        self.browser.get(self.live_server_url)
        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate_to_admin_page()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_page = AdminArticlePage(self.browser)
        admin_page.add_new_article(self.article)

        self.browser.get(self.live_server_url)
        main_page = MainPage(self.browser)
        self.assertTrue(main_page.is_article_visible(self.article["title"]))
    
    def test_edit_article(self):
        """Tests that it's possible to edit existing article via admin panel.
        """
        changes = {"content": "Edited Content"}
        article = self.create_dummy_article(self.article)

        self.browser.get(self.live_server_url)
        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate_to_admin_page()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_page = AdminArticlePage(self.browser)
        admin_page.edit_article(article.title, changes)

        self.browser.get(self.live_server_url)
        article_page = ArticlePage(self.browser)
        article_page.navigate_to_article(article.title)
        self.assertTrue(changes["content"] == article_page.get_content())
    
    def test_delete_article(self):
        """Test that it's possible to remove existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)

        self.browser.get(self.live_server_url)
        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate_to_admin_page()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_page = AdminArticlePage(self.browser)
        admin_page.delete_article(article.title)

        self.browser.get(self.live_server_url)
        main_page = MainPage(self.browser)
        self.assertFalse(main_page.is_article_visible(article.title))

    def test_displays_article_page(self):
        """Tests that article page is displayed correctly
        with following sections:
        - Title
        - Publish date
        - Content
        """
        article = self.create_dummy_article(self.article)
        self.browser.get(self.live_server_url)
        article_page = ArticlePage(self.browser)
        article_page.navigate_to_article(article.title)

        expected_article = {
            "title": self.article["title"],
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "content": self.article["content"]
        }
        self.assertDictEqual(article_page.to_dict(), expected_article)
    
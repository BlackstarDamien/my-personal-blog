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
        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_page = AdminArticlePage(self.browser)
        admin_page.add_new_article(self.article)

        main_page = MainPage(self.browser).navigate()
        self.assertTrue(main_page.is_article_visible(self.article["title"]))

        article_page = ArticlePage(self.browser).navigate(self.article["title"])
        self.assertDictEqual(article_page.to_dict(), self.article)
    
    def test_edit_article(self):
        """Tests that it's possible to edit existing article via admin panel.
        """
        changes = {"content": "Edited Content"}
        article = self.create_dummy_article(self.article)

        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_page = AdminArticlePage(self.browser)
        admin_page.edit_article(article.title, changes)

        article_page = ArticlePage(self.browser).navigate(article.title)
        self.assertTrue(changes["content"] == article_page.get_content())
    
    def test_delete_article(self):
        """Test that it's possible to remove existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)

        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_page = AdminArticlePage(self.browser)
        admin_page.delete_article(article.title)

        main_page = MainPage(self.browser).navigate()
        self.assertFalse(main_page.is_article_visible(article.title))

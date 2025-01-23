from blog.tests.e2e.base import TestBase
from pathlib import Path

from .pages.article_page import ArticlePage
from .pages.main_page import MainPage
from .pages.admin_login_page import AdminLoginPage


class TestArticles(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_create_article(self):
        """Tests that it's possible to add an article via admin panel.
        """
        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_articles_page = admin_page.navigate_to_articles()
        admin_articles_page.add_new_article(self.article).save()

        main_page = MainPage(self.browser).navigate()
        self.assertTrue(main_page.is_article_visible(self.article["title"]))

        article_page = ArticlePage(self.browser).navigate(self.article["title"])
        self.assertDictEqual(article_page.to_dict(), self.article)
    
    def test_edit_article(self):
        """Tests that it's possible to edit existing article via admin panel.
        """
        changes = {"content": "Edited Content"}
        article = self.create_dummy_article(self.article)

        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_articles_page = admin_page.navigate_to_articles()
        admin_articles_page.edit_article(article.title, changes)

        article_page = ArticlePage(self.browser).navigate(article.title)
        self.assertTrue(changes["content"] == article_page.get_content())
    
    def test_delete_article(self):
        """Test that it's possible to remove existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)

        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_articles_page = admin_page.navigate_to_articles()
        admin_articles_page.delete_article(article.title)

        main_page = MainPage(self.browser).navigate()
        self.assertFalse(main_page.is_article_visible(article.title))

    def test_can_handle_markdown_format(self):
        """Test that it's possible to handle content written in Markdown"""
        md_article = {
            "title": "Test Article",
            "publish_date": "2024-10-11",
            "content": """# Some good title\n## Part One\nThis is part one"""
        }
        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_articles_page = admin_page.navigate_to_articles()
        admin_articles_page.add_new_article(md_article).save()

        article_page = ArticlePage(self.browser).navigate(self.article["title"])
        content = article_page.get_content()

        expected = """Some good title\nPart One\nThis is part one"""
        self.assertEqual(content, expected)
    
    def test_can_display_images_inside_article(self):
        """Tests that it's possible to render all images inside an article.
        """
        article = {
            "title": "Test Article With Image",
            "publish_date": "2024-10-11",
        }

        with open(Path(__file__).parent.parent / "data/article-with-image.md") as f:
            article["content"] = f.read()
        
        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        admin_articles_page = admin_page.navigate_to_articles()

        path_to_image = Path(__file__).parent.parent / "data/black-cat.jpg"
        admin_articles_page.add_new_article(article).attach_images(path_to_image).save()

        article_page = ArticlePage(self.browser).navigate(self.article["title"])
        images = article_page.get_all_images()

        self.assertEqual(len(images), 1)
        self.assertEqual((images[0].text), "black-cat.jpg")

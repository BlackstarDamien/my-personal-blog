from blog.tests.e2e.base import TestBase
from django.test import override_settings

from blog.models import Article, Image
from .pages.article_page import ArticlePage
from .pages.main_page import MainPage
from blog.tests.helpers import (
    create_dummy_article, create_dummy_image
)


STORAGE_TEST_OPTIONS = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage"
    }
}


class TestArticles(TestBase):
    def setUp(self) -> None:
        super().setUp()
    
    def test_display_article(self):
        """Tests created articles is displayed under it's own URL.
        """
        create_dummy_article(self.article)
        main_page = MainPage(self.browser).navigate()
        self.assertTrue(main_page.is_article_visible(self.article["title"]))

        article_page = ArticlePage(self.browser).navigate(self.article["title"])
        self.assertDictEqual(article_page.to_dict(), self.article)
    
    def test_can_handle_markdown_format(self):
        """Test that it's possible to handle content written in Markdown"""
        md_article = {
            "title": "Test Article",
            "publish_date": "2024-10-11",
            "content": """# Some good title\n## Part One\nThis is part one"""
        }

        create_dummy_article(md_article)
        article_page = ArticlePage(self.browser).navigate(md_article["title"])
        content = article_page.get_content()

        expected = """Some good title\nPart One\nThis is part one"""
        self.assertEqual(content, expected)
    
    @override_settings(STORAGES=STORAGE_TEST_OPTIONS)
    def test_can_display_images_inside_article(self):
        """Tests that it's possible to render all images inside an article.
        """
        md_content = "\n".join([
            "## This is an article with image",
            "### Overview",
            "This article was created to display a single image",
            "Here's an photography of this tiny little cat:",
            "![](black-cat.jpg)"
        ])
        article = {
            "title": "Article With Image",
            "publish_date": "2024-10-11",
            "content": md_content 
        }
        self.create_article_with_image(article)
        article_page = ArticlePage(self.browser).navigate(article["title"])
        images = article_page.get_all_images()

        self.assertEqual(len(images), 1)
        image_name = images[0].get_attribute("src").split("/")[-1]
        self.assertRegex(image_name, r"black-cat(\_.*)?\.jpg")

    def create_article_with_image(self, article: dict):
        md_article = create_dummy_article(article)
        articles_image = create_dummy_image("black-cat.jpg")
        self.__bind_image_with_article(articles_image, md_article)

    def __bind_image_with_article(self, image: Image, article: Article) -> Image:
        image.article = article
        image.save()
        return image

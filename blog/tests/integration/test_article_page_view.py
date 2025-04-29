from django.test import TestCase, override_settings
from blog.models import Article, Image
from django.conf import settings
from blog.tests.helpers import (
    create_dummy_image,
    create_dummy_article
)


STORAGE_TEST_OPTIONS = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage"
    }
}

class TestArticlePageView(TestCase):
    def setUp(self) -> None:
        self.article = create_dummy_article(
            {
                "title": "Test Article",
                "content": """# Test title\nTest content"""
            }
        )
        self.article_url = self.article.get_absolute_url()
    
    def test_article_page_returns_correct_html(self):
        """Test that article page returns proper html file.
        """
        response = self.client.get(self.article_url)
        self.assertTemplateUsed(response, 'article.html')

    def test_articles_page_receives_proper_context_data(self):
        """Tests that article page returns proper data in context.
        """
        response = self.client.get(self.article_url)
        self.assertEqual(self.article, response.context["article"])

    def test_article_page_handle_markdown_content(self):
        """Tests that article page properly converts Markdown format."""
        response = self.client.get(self.article_url)
        expected = """<h1>Test title</h1>\n<p>Test content</p>"""

        self.assertInHTML(expected, str(response.content))

    @override_settings(STORAGES=STORAGE_TEST_OPTIONS)
    def test_article_page_handle_images(self):
        """Tests that article page is able to display images.
        """
        img_file_name = "test_file.jpg"
        self.__attach_content_with_image(img_file_name)

        test_image = create_dummy_image(img_file_name)
        self.__bind_image_with_article(test_image, self.article)
        response = self.client.get(self.article_url)

        image_path = settings.MEDIA_URL + str(test_image.url)
        expected = f"""<img alt="" src="{image_path}">"""
        self.assertInHTML(expected, str(response.content))

    def __attach_content_with_image(self, img_file_name: str):
        content_with_img = f"Here's a nice picture: ![]({img_file_name})"
        self.article.content += content_with_img
        self.article.save()

    def __bind_image_with_article(self, image: Image, article: Article) -> Image:
        image.article = article
        image.save()
        return image


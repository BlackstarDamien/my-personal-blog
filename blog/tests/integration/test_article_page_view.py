from io import BytesIO
from PIL import Image as PILImage
from django.test import TestCase, override_settings
from blog.models import Article, Image
from pathlib import Path
from django.core.files.images import ImageFile
from django.conf import settings


STORAGE_TEST_OPTIONS = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage"
    }
}

class TestArticlePageView(TestCase):
    def setUp(self) -> None:
        self.article = Article.objects.create(
            title="Test Article 1",
            content="Test Content"
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
        md_article = Article.objects.create(
            title="Test Article MD",
            content="""# Test title\nTest content"""
        )

        md_article_url = md_article.get_absolute_url()
        response = self.client.get(md_article_url)
        expected = """<h1>Test title</h1>\n<p>Test content</p>"""

        self.assertInHTML(expected, str(response.content))

    @override_settings(STORAGES=STORAGE_TEST_OPTIONS)
    def test_article_page_handle_images(self):
        """Tests that article page is able to display images.
        """
        img_file_name = "test_file.jpg"
        with open(Path(__file__).parent.parent / "data/article-with-image.md") as f:
            article_content = f.read().format(img_file_name=img_file_name)

        article = Article.objects.create(
            title="Test Article With Image",
            content=article_content
        )
        article_image = self.create_test_image(img_file_name, article)
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)

        image_path = settings.MEDIA_URL + str(article_image.url)
        expected = f"""<img alt="" src="{image_path}">"""
        self.assertInHTML(expected, str(response.content))

    def create_test_image(self, file_name: str, article: Article) -> Image:
        """Creates instance of Image model for testing purpose.

        Parameters
        ----------
        file_name : str
            Name of the file
        article : Article
            Instance of Article that Image is attached to

        Returns
        -------
        Image
            Instace of Image model
        """
        test_image_content = self.__create_temp_img_content()
        image_file = ImageFile(
                file=test_image_content,
                name=file_name
        )

        article_image = Image(
            name=file_name,
            url=image_file,
            article=article
        )
        article_image.save()

        return article_image
    
    def __create_temp_img_content(self) -> BytesIO:
        temp_img = BytesIO()
        image = PILImage.new(
            mode="RGB",
            size=(200, 200),
            color=(255, 0, 0, 0)
        )
        image.save(temp_img, "jpeg")
        temp_img.seek(0)
        return temp_img

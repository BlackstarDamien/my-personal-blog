from io import BytesIO
from PIL import Image as PILImage
from django.test import TestCase, override_settings
from blog.models import Article, Image
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
            content="""# Test title\nTest content"""
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
        content_with_img = f"Here's a nice picture: ![]({img_file_name})"
        self.article.content += content_with_img
        self.article.save()

        test_image = self.create_test_image(img_file_name)
        self.bind_image_with_article(test_image, self.article)
        response = self.client.get(self.article_url)

        image_path = settings.MEDIA_URL + str(test_image.url)
        expected = f"""<img alt="" src="{image_path}">"""
        self.assertInHTML(expected, str(response.content))

    def bind_image_with_article(self, image: Image, article: Article) -> Image:
        """Binds instance of Image model with instance of Article model.

        Parameters
        ----------
        image : Image
            Instance of Image model
        article : Article
            Dependant instance of Article model

        Returns
        -------
        Image
            Image model's object with attached Article
        """
        image.article = article
        image.save()
        return image

    def create_test_image(self, file_name: str) -> Image:
        """Creates instance of Image model for testing purpose.

        Parameters
        ----------
        file_name : str
            Name of the file

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
        )

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

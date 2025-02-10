import os
from django.test import TestCase
from blog.models import Article, Image
from pathlib import Path
from django.core.files.images import ImageFile
from django.conf import settings


class TestArticlePageView(TestCase):
    def setUp(self) -> None:
        self.article = Article.objects.create(
            title="Test Article 1",
            content="Test Content"
        )
        self.article_url = self.article.get_absolute_url()
    
    def tearDown(self):
        if os.path.exists("images/black-cat.jpg"):
            os.remove("images/black-cat.jpg")
    
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

    def test_article_page_handle_images(self):
        """Tests that article page is able to display images.
        """
        with open(Path(__file__).parent.parent / "data/article-with-image.md") as f:
            article_content = f.read()

        article_with_images = Article.objects.create(
            title="Test Article With Image",
            content=article_content
        )

        path_to_image = Path(__file__).parents[1] / "data/black-cat.jpg"
        with path_to_image.open(mode='rb') as f:
            article_image = Image()
            article_image.article = article_with_images
            article_image.name = "black-cat.jpg"
            article_image.url = ImageFile(f, name=path_to_image.name)
            article_image.save()

        image_path = settings.MEDIA_URL + str(article_image.url)
        article_url = article_with_images.get_absolute_url()
        response = self.client.get(article_url)
        expected = f"""<img alt="" src="{image_path}">"""

        self.assertInHTML(expected, str(response.content))

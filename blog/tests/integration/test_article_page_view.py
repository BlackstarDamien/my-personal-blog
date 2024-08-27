from django.test import TestCase
from blog.models import Article


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

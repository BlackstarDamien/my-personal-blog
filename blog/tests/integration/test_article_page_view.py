from typing import List
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.views import article_page
from blog.models import Article


class TestArticlePageView(TestCase):
    def setUp(self) -> None:
        self.article = Article.objects.create(
            title="Test Article 1",
            content="Test Content"
        )
    
    def test_article_page_returns_correct_html(self):
        """Test that main page returns proper html file.
        """
        request = HttpRequest()
        reponse = article_page(request, self.article.slug)
        expected_html = render_to_string('article.html')
        self.assertEqual(reponse.content.decode(), expected_html)

    def test_articles_page_receives_proper_context_data(self):
        """Tests that article page returns proper data in context.
        """
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(self.article, response.context["article"])

from typing import List
from django.test import TestCase
from django.http import HttpResponse
from django.template.loader import render_to_string
from blog.models import Article


class TestMainPageView(TestCase):
    def test_main_page_returns_correct_html(self):
        """Test that main page returns proper html file.
        """
        response = self.call_main_page()
        expected_html = render_to_string('index.html')
        self.assertEqual(response.content.decode(), expected_html)
    
    def test_main_page_rendered_with_data(self):
        """Tests that main page is rendered with data properly.
        """
        expected_articles = self.create_dummy_articles()
        response = self.call_main_page()
        fetched_articles = list(response.context['articles'])
        self.assertListEqual(fetched_articles, expected_articles)

    def call_main_page(self) -> HttpResponse:
        return self.client.get('/')

    def create_dummy_articles(self) -> List[Article]:
        """Creates dummy articles.

        Returns:
            List[Article]: Created dummy articles.
        """
        test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]
        articles = [Article.objects.create(**article) for article in test_articles]
        return articles

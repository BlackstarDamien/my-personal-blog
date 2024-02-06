from typing import List
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.views import main_page
from blog.models import Article


class TestMainPageView(TestCase):
    def test_main_page_returns_correct_html(self):
        """Test that main page returns proper html file.
        """
        request = HttpRequest()
        reponse = main_page(request)
        expected_html = render_to_string('index.html')
        self.assertEqual(reponse.content.decode(), expected_html)
    
    def test_main_page_rendered_with_data(self):
        """Tests that main page is rendered with data properly.
        """
        expected_articles = self.create_dummy_articles()
        request = HttpRequest()
        reponse = main_page(request)
        self.assertTrue(
            all(article in reponse.content.decode() 
                for article in expected_articles))

    
    def create_dummy_articles(self) -> List[str]:
        """Creates dummy articles.

        Returns:
            List[Dict[str, str]]: Created dummy articles.
        """
        test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]
        for article in test_articles:
            Article.objects.create(**article)
        
        return [article["title"] for article in test_articles]

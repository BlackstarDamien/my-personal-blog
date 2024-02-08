from typing import List
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.views import article_page


class TestArticlePageView(TestCase):
    def test_article_page_returns_correct_html(self):
        """Test that main page returns proper html file.
        """
        request = HttpRequest()
        reponse = article_page(request)
        expected_html = render_to_string('article.html')
        self.assertEqual(reponse.content.decode(), expected_html)

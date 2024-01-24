from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.views import main_page


class TestMainPageView(TestCase):
    def test_main_page_returns_correct_html(self):
        """Test that main page returns proper html file.
        """
        request = HttpRequest()
        reponse = main_page(request)
        expected_html = render_to_string('index.html')
        self.assertEquals(reponse.content.decode(), expected_html)

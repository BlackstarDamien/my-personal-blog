from django.test import TestCase, Client
from django.urls import path, clear_url_caches
from blog.views import server_error_view
from blog.urls import urlpatterns
from blog.tests.helpers.functions import trigger_500_error


class Test500Page(TestCase):
    """Integration tests for 500 error page."""

    def setUp(self):
        self.client = Client(raise_request_exception=False)

        urlpatterns.append(
            path(
                'trigger-500-error', 
                trigger_500_error, 
                name='trigger_500_error'
            )
        )
        clear_url_caches()

    def test_500_page_returns_correct_status_code(self):
        """Test 500 error page view returns correct status code."""
        response = server_error_view(self.client.get('/trigger-500-error'))
        self.assertEqual(response.status_code, 500)

    def test_500_page_uses_correct_template(self):
        """Test that 500 error page uses proper template."""
        response = self.client.get('/trigger-500-error')
        self.assertTemplateUsed(response, '500.html')

    def test_500_page_contains_error_message(self):
        """Test that 500 error page contains appropriate error message."""
        response = self.client.get('/trigger-500-error')
        self.assertContains(
            response, 
            "Something went wrong on our end", 
            status_code=500
        )

    def test_500_page_content_type(self):
        """Test that 500 error page returns HTML content type."""
        response = server_error_view(self.client.get('/trigger-500-error'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

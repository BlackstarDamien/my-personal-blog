from django.test import TestCase, Client


class Test404Page(TestCase):
    """Integration tests for 404 error page."""

    def setUp(self):
        self.client = Client(raise_request_exception=False)

    def test_404_page_returns_correct_status_code(self):
        """Test that a non-existent URL returns 404 status code."""
        response = self.client.get('/non-existent-page-that-does-not-exist/')
        self.assertEqual(response.status_code, 404)

    def test_404_page_uses_correct_template(self):
        """Test that 404 page uses the custom 404 template."""
        response = self.client.get('/non-existent-page-that-does-not-exist/')
        self.assertTemplateUsed(response, '404.html')

    def test_404_page_contains_error_message(self):
        """Test that 404 page contains appropriate error message."""
        response = self.client.get('/non-existent-page-that-does-not-exist/')
        self.assertContains(response, "Page Not Found", status_code=404)

    def test_404_page_contains_home_link(self):
        """Test that 404 page contains a link back to home."""
        response = self.client.get('/non-existent-page-that-does-not-exist/')
        self.assertContains(response, 'href="/"', status_code=404)

    def test_404_for_invalid_blog_post_slug(self):
        """Test that invalid blog post slug returns 404."""
        response = self.client.get('/articles/this-post-does-not-exist/')
        self.assertEqual(response.status_code, 404)

    def test_404_page_content_type(self):
        """Test that 404 page returns HTML content type."""
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_404_with_special_characters_in_url(self):
        """Test 404 handling with special characters in URL."""
        response = self.client.get('/page-with-special-chars-!@#$/')
        self.assertEqual(response.status_code, 404)

    def test_404_with_long_url(self):
        """Test 404 handling with very long URL."""
        long_path = '/a' * 500 + '/'
        response = self.client.get(long_path)
        self.assertIn(response.status_code, [404, 414])  # 414 is URI Too Long

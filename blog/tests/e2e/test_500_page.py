from django.http import HttpRequest, HttpResponse
from django.test import override_settings
from django.urls import clear_url_caches, path
from blog.tests.e2e.base import TestBase
from blog.urls import urlpatterns
from .pages.server_error_page import ServerErrorPage

def trigger_500_error(request: HttpRequest) -> HttpResponse:
    raise Exception("Intentional server error for testing purposes")

class Test500Page(TestBase):
    def setUp(self) -> None:
        super().setUp()
        urlpatterns.append(
            path('trigger-500-error', trigger_500_error, name='trigger_500_error')
        )
        clear_url_caches()

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_500_page_displayed_for_server_error(self):
        """Navigate to error trigger URL and verify 500 page is displayed."""
        server_error_page = ServerErrorPage(self.page).navigate_to_error_trigger()
        self.assertEqual(server_error_page.get_title(), "Server Error")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_500_page_error_message_is_displayed(self):
        """Verify the error message content is correct."""
        server_error_page = ServerErrorPage(self.page).navigate_to_error_trigger()
        self.assertIn(
            "Something went wrong on our end. Please try again later.",
            server_error_page.get_error_message(),
        )

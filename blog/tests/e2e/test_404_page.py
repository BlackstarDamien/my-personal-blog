from django.test import override_settings
from blog.tests.e2e.base import TestBase
from .pages.non_existent_page import NonExistentPage


class Test404Page(TestBase):
    def setUp(self) -> None:
        super().setUp()

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_404_page_displayed_for_non_existent_article(self):
        """Navigate to non-existent article URL and verify 404 page is displayed."""
        non_existent_page = NonExistentPage(self.page).navigate_to_fake_article()
        self.assertEqual(non_existent_page.get_title(), "Page Not Found")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_404_page_error_message_is_displayed(self):
        """Verify the error message content is correct."""
        non_existent_page = NonExistentPage(self.page).navigate_to_fake_article()
        self.assertIn(
            "The page you are looking for does not exist.",
            non_existent_page.get_error_message(),
        )

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_home_link_navigates_to_homepage(self):
        """Verify the Home link is present and functional."""
        non_existent_page = NonExistentPage(self.page).navigate_to_fake_article()
        home_page = non_existent_page.click_home_link()
        self.assertEqual(home_page.get_title(), "My Personal Blog")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["*"])
    def test_404_for_non_existent_static_page(self):
        """Verify 404 works for static pages, not just articles."""
        non_existent_page = NonExistentPage(self.page).navigate_to_fake_static_page()
        self.assertEqual(non_existent_page.get_title(), "Page Not Found")
        
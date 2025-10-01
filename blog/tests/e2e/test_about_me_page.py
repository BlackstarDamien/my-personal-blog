from blog.tests.e2e.base import TestBase
from .pages.about_me_page import AboutMePage
from blog.tests.helpers import create_dummy_about_me


class TestAboutMePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
    
    def test_display_about_me_page(self):
        """Tests that About Me page is displayed properly.
        """
        create_dummy_about_me(self.about_me)
        about_me_page = AboutMePage(self.page).navigate()

        self.assertDictEqual(about_me_page.to_dict(), self.about_me)
    
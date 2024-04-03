from blog.tests.e2e.base import TestBase
from .pages.admin_login_page import AdminLoginPage
from .pages.admin_page import AdminAboutMePage
from .pages.main_page import MainPage


class TestAboutMePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_fill_about_me_page(self):
        """Tests that it's possible to fill about me page via admin panel.
        """
        self.browser.get(self.live_server_url)
        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate_to_admin_page()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_about_me_page = AdminAboutMePage(self.browser)
        admin_about_me_page.fill_content(self.about_me)

        self.browser.get(self.live_server_url)
        main_page = MainPage(self.browser)
        about_me_page = main_page.go_to_about_me_page()
        self.assertDictEqual(about_me_page.to_dict(), self.about_me)
    
    def test_edit_about_me_page(self):
        """Tests that it's possible to edit existing about me page
        via admin panel.
        """
        self.create_dummy_about_me_page(self.about_me)
        change = {"content": "Edited about me"}

        self.browser.get(self.live_server_url)
        admin_login_page = AdminLoginPage(self.browser)
        admin_login_page.navigate_to_admin_page()
        admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_about_me_page = AdminAboutMePage(self.browser)
        admin_about_me_page.edit(change)

        self.browser.get(self.live_server_url)
        main_page = MainPage(self.browser)
        about_me_page = main_page.go_to_about_me_page()

        self.assertEqual(about_me_page.get_content(), change["content"])

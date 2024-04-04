from blog.tests.e2e.base import TestBase
from .pages.admin_login_page import AdminLoginPage
from .pages.about_me_page import AboutMePage


class TestAboutMePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_fill_about_me_page(self):
        """Tests that it's possible to fill about me page via admin panel.
        """
        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_about_me_page = admin_page.navigate_to_about_me()
        admin_about_me_page.fill_content(self.about_me)

        about_me_page = AboutMePage(self.browser).navigate()

        self.assertDictEqual(about_me_page.to_dict(), self.about_me)
    
    def test_edit_about_me_page(self):
        """Tests that it's possible to edit existing about me page
        via admin panel.
        """
        self.create_dummy_about_me_page(self.about_me)
        change = {"content": "Edited about me"}

        admin_login_page = AdminLoginPage(self.browser).navigate()
        admin_page = admin_login_page.login(self.admin["username"], self.admin["password"])
        
        admin_about_me_page = admin_page.navigate_to_about_me()
        admin_about_me_page.edit(change)

        about_me_page = AboutMePage(self.browser).navigate()
        self.assertEqual(about_me_page.get_content(), change["content"])

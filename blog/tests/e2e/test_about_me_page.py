from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase


class TestAboutMePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_fill_about_me_page(self):
        """Tests that it's possible to fill about me page via admin panel.
        """
        self.given_a_page("Admin")

        self.when_logs_into_admin_page()
        self.when_click_link('About me')

        self.then_i_can_see_admin_list_page("About me")
        self.then_i_will_click_on_add_button("About me")
        self.then_i_will_add_new_page(self.about_me)
        self.then_page_is_visible_on_admin_page(self.about_me["title"])
    
    def test_edit_about_me_page(self):
        """Tests that it's possible to edit existing about me page
        via admin panel.
        """
        about_me = self.create_dummy_about_me_page(self.about_me)
        self.given_a_page("Admin")

        self.when_logs_into_admin_page()
        self.when_click_link('About me')
        self.when_click_link(about_me.title)

        self.then_i_can_see_admin_edit_about_me_form(about_me.title)
        self.then_i_will_edit_existing_page({"content": "Edited about me"})
        self.then_i_can_see_admin_list_page("About Me")

    def test_displays_about_me_page(self):
        """Tests that About Me page is displayed correctly.
        """
        self.create_dummy_about_me_page(self.about_me)
        self.given_a_page("Main")
        self.when_click_link("About Me")
        self.then_i_can_see_about_me_page()

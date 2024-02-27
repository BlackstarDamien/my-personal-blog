from typing import Dict

from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase


class TestAboutMePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.about_me = {
            "title": "About Me",
            "content": "Something about me"
        }
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
        self.then_i_can_see_admin_list_page("About Me")
    
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
        self.then_i_will_edit_about_me_page({"content": "Edited about me"})

    def test_displays_about_me_page(self):
        """Tests that About Me page is displayed correctly.
        """
        self.create_dummy_about_me_page(self.about_me)
        self.given_a_page("Main")
        self.when_click_link("About Me")
        self.then_i_can_see_about_me_page()
    
    def test_clicking_on_logo_redirects_to_main_page(self):
        """Tests that clicking on blog's name redirect user
        to the main page.
        """
        self.given_a_page("About me")
        self.when_click_link("My Personal Blog")
        self.then_i_am_on_the_main_page()
    
    def then_i_can_see_about_me_page(self):
        """Checks if About Me page is displayed properly.
        """
        expected_url = f"{self.live_server_url}/about-me"
        self.assertEqual(expected_url, self.browser.current_url)

        title = self.browser.find_element(By.CSS_SELECTOR, ".about_me-title")
        content = self.browser.find_element(By.CSS_SELECTOR, ".about_me-content")
        
        current_about_me = {
            "title": title.text,
            "content": content.text
        }
        expected_about_me = {
            "title": self.about_me["title"],
            "content": self.about_me["content"]
        }
        self.assertDictEqual(current_about_me, expected_about_me)

    def then_i_will_edit_about_me_page(self, changes: Dict[str, str]):
        """Edit properties of About Me Page.

        Args:
            changes (Dict[str, str]): Fields to change with new values.
        """
        for k in changes:
            field_to_change = self.browser.find_element(By.NAME, k)
            field_to_change.clear()
            field_to_change.send_keys(changes[k])
        
        self.browser.find_element(By.NAME, "_save").click()
        self.then_i_can_see_admin_list_page("About Me")

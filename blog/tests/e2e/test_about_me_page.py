from typing import Dict

from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase
from django.contrib.auth.models import User
from blog.models import AboutMe


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
        self.given_an_admin_page()
        self.when_click_link('About me')
        self.then_i_am_on_the_page("admin", "About me")
        self.then_i_will_click_on_add_button("About me")
        self.then_i_will_add_about_me(self.about_me)
    
    def test_edit_about_me_page(self):
        """Tests that it's possible to edit existing about me page
        via admin panel.
        """
        about_me = self.create_dummy_about_me_page(self.about_me)
        self.given_an_admin_page()
        self.when_click_link('About me')
        self.when_click_link(about_me.title)
        self.then_i_am_on_the_page("edit_about_me", about_me.title)
        self.then_i_will_edit_about_me_page({"content": "Edited about me"})

    def test_displays_about_me_page(self):
        """Tests that About Me page is displayed correctly.
        """
        self.create_dummy_about_me_page(self.about_me)
        self.given_a_main_page()
        self.when_click_link("About Me")
        self.then_i_can_see_about_me_page()
    
    def test_clicking_on_logo_redirects_to_main_page(self):
        """Tests that clicking on blog's name redirect user
        to the main page.
        """
        self.given_an_about_me_page()
        self.when_click_link("My Personal Blog")
        self.then_i_am_on_the_page("main")
    
    def given_an_about_me_page(self):
        self.browser.get(f"{self.live_server_url}/about-me")
    
    def given_an_admin_page(self):
        """Goes and logs into admin page."""
        self.browser.get(self.live_server_url + '/admin/')

        username_input = self.browser.find_element(By.ID,'id_username')
        username_input.send_keys(self.admin["username"])
        password_input = self.browser.find_element(By.ID,'id_password')
        password_input.send_keys(self.admin["password"])

        self.browser.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertIn('Site administration', self.browser.title)
    
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
    
    def create_dummy_about_me_page(self, data: Dict[str, str]):
        return AboutMe.objects.create(**data)
    
    def create_dummy_admin_user(self):
        """Create Admin user for testing purpose.
        """
        self.admin = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "adm1n"
        }
        User.objects.create_superuser(**self.admin)
    
    def then_i_will_add_about_me(self, new_about_me: Dict[str, str]):
        """Fill add article form, submits and checks if was created.

        Args:
            new_article (Dict[str, str]): New article's details.
        """
        title_field = self.browser.find_element(By.NAME, 'title')
        content_field = self.browser.find_element(By.NAME, 'content')

        title_field.send_keys(new_about_me["title"])
        content_field.send_keys(new_about_me["content"])
        self.browser.find_element(By.NAME, "_save").click()

        self.then_i_am_on_the_page("admin", "About Me")

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
        self.then_i_am_on_the_page("admin", "About Me")

from typing import Dict

from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase
from blog.models import AboutMe


class TestAboutMePage(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.about_me = {
            "title": "About Me",
            "content": "Something about me"
        }
        self.create_dummy_about_me_page(self.about_me)
    
    def test_displays_about_me_page(self):
        """Tests that About Me page is displayed correctly.
        """
        self.given_a_main_page()
        self.when_click_link("About Me")
        self.then_i_can_see_about_me_page()
    
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
    
    # Write test that checks if you can nagivate to main paga via logo
    
    def create_dummy_about_me_page(self, data: Dict[str, str]):
        AboutMe.objects.create(**data)
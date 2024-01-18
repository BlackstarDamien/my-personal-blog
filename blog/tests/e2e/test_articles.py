from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from django.test import LiveServerTestCase


class TestArticles(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestArticles, cls).setUpClass()
        cls.admin = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "adm1n"
        }
        User.objects.create_superuser(**cls.admin)

    def setUp(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.implicitly_wait(3)

        self.data = {
            "title": "Test Article",
            "content": "Test Content"
        }

    def tearDown(self) -> None:
        self.browser.close()

    def test_create_article(self):
        """Tests that it's possible to add an article via admin panel.
        """
        self.given_an_admin_page()
        self.when_click_link('Articles')
        self.then_i_am_on_the_admin_page('Article')
        self.then_i_will_click_on_add_button('Article')
        self.then_i_will_add_new_article(self.data)
    
    def given_an_admin_page(self):
        """Goes and logs into admin page."""
        self.browser.get(self.live_server_url + '/admin/')

        username_input = self.browser.find_element(By.ID,'id_username')
        username_input.send_keys(self.admin["username"])
        password_input = self.browser.find_element(By.ID,'id_password')
        password_input.send_keys(self.admin["password"])

        self.browser.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertIn('Site administration', self.browser.title)

    def when_click_link(self, link_text: str):
        """Clicks on given link name.

        Args:
            link_text (str): Name of link to click.
        """
        self.browser.find_element(By.LINK_TEXT, link_text).click()
    
    def then_i_am_on_the_admin_page(self, page_name: str):
        """Check if user is on given admin page.

        Args:
            page_name (str): Admin's page name.
        """
        name = page_name.lower()
        expected_name = f"Select {name} to change | Django site admin"
        self.assertEquals(expected_name, self.browser.title)
    
    def then_i_will_click_on_add_button(self, button_name: str):
        """Clicks on given add button and redirect to create form.

        Args:
            button_name (str): Name of add button to click.
        """
        name = button_name.lower()

        self.browser.refresh()
        self.browser.find_element(By.XPATH, f"//a[@href='/admin/blog/{name}/add/']").click()
        
        self.assertEquals("Add article | Django site admin", self.browser.title)
    
    def then_i_will_add_new_article(self, new_article: Dict[str, str]):
        """Fill add article form, submits and checks if was created.

        Args:
            new_article (Dict[str, str]): New article's details.
        """
        title_field = self.browser.find_element(By.NAME, 'title')
        content_field = self.browser.find_element(By.NAME, 'content')

        title_field.send_keys(new_article["title"])
        content_field.send_keys(new_article["content"])
        self.browser.find_element(By.NAME, "_save").click()

        self.then_i_am_on_the_admin_page('article')

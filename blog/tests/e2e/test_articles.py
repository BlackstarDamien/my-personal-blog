from typing import Dict

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from blog.tests.e2e.base import TestBase


class TestArticles(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_create_article(self):
        """Tests that it's possible to add an article via admin panel.
        """
        self.given_an_admin_page()
        self.when_click_link('Articles')
        self.then_i_am_on_the_page("admin", "Article")
        self.then_i_will_click_on_add_button('Article')
        self.then_i_will_add_new_article(self.article)
    
    def test_edit_article(self):
        """Tests that it's possible to edit existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)
        self.given_an_admin_page()
        self.when_click_link('Articles')
        self.when_click_link(article.title)
        self.then_i_am_on_the_page("edit_article", article.title)
        self.then_i_will_edit_existing_article({"content": "Edited Content"})
    
    def test_delete_article(self):
        """Test that it's possible to remove existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)
        self.given_an_admin_page()
        self.when_click_link('Articles')
        self.when_click_link(article.title)
        self.then_i_am_on_the_page("edit_article", article.title)
        self.then_i_will_remove_existing_article(article.id)
        self.then_article_is_not_present(article.title)

    def create_dummy_admin_user(self):
        """Create Admin user for testing purpose.
        """
        self.admin = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "adm1n"
        }
        User.objects.create_superuser(**self.admin)

    def given_an_admin_page(self):
        """Goes and logs into admin page."""
        self.browser.get(self.live_server_url + '/admin/')

        username_input = self.browser.find_element(By.ID,'id_username')
        username_input.send_keys(self.admin["username"])
        password_input = self.browser.find_element(By.ID,'id_password')
        password_input.send_keys(self.admin["password"])

        self.browser.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertIn('Site administration', self.browser.title)
    
    def then_i_will_click_on_add_button(self, button_name: str):
        """Clicks on given add button and redirect to create form.

        Args:
            button_name (str): Name of add button to click.
        """
        name = button_name.lower()

        self.browser.refresh()
        self.browser.find_element(By.XPATH, f"//a[@href='/admin/blog/{name}/add/']").click()
        
        self.assertEqual("Add article | Django site admin", self.browser.title)
    
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

        self.then_i_am_on_the_page("admin", "Article")

    def then_i_will_edit_existing_article(self, changes: Dict[str, str]):
        """Edit properties of existing article.

        Args:
            changes (Dict[str, str]): Fields to change with new values.
        """
        for k in changes:
            field_to_change = self.browser.find_element(By.NAME, k)
            field_to_change.clear()
            field_to_change.send_keys(changes[k])
        
        self.browser.find_element(By.NAME, "_save").click()
        self.then_i_am_on_the_page("admin", "Article")

    def then_i_will_remove_existing_article(self, id: int):
        """Removes existing article.
        """
        delete_link = f"//a[@href='/admin/blog/article/{id}/delete/']"
        self.browser.find_element(By.XPATH, delete_link).click()
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()
        self.then_i_am_on_the_page("admin", "Article")
    
    def then_article_is_not_present(self, title: str):
        """Checks if article exists in admin page.

        Args:
            title (str): Title of article to check.
        """
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.LINK_TEXT, title)

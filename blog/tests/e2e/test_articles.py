from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from django.template.defaultfilters import slugify
from blog.tests.e2e.base import TestBase


class TestArticles(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.create_dummy_admin_user()
    
    def test_create_article(self):
        """Tests that it's possible to add an article via admin panel.
        """
        self.given_a_page("Admin")

        self.when_logs_into_admin_page()
        self.when_click_link('Articles')

        self.then_i_can_see_admin_list_page("Article")
        self.then_i_will_click_on_add_button('Article')
        self.then_i_will_add_new_page(self.article)
        self.then_page_is_visible_on_admin_page(self.article["title"])
    
    def test_edit_article(self):
        """Tests that it's possible to edit existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)
        self.given_a_page("Admin")

        self.when_logs_into_admin_page()
        self.when_click_link('Articles')
        self.when_click_link(article.title)

        self.then_i_can_see_admin_edit_article_form(article.title)
        self.then_i_will_edit_existing_page({"content": "Edited Content"})
        self.then_i_can_see_admin_list_page("Article")
    
    def test_delete_article(self):
        """Test that it's possible to remove existing article via admin panel.
        """
        article = self.create_dummy_article(self.article)
        self.given_a_page("Admin")

        self.when_logs_into_admin_page()
        self.when_click_link('Articles')
        self.when_click_link(article.title)

        self.then_i_can_see_admin_edit_article_form(article.title)
        self.then_i_will_remove_existing_article(article.id)
        self.then_article_is_not_present(article.title)

    def test_displays_article_page(self):
        """Tests that article page is displayed correctly
        with following sections:
        - Title
        - Publish date
        - Content
        """
        article = self.create_dummy_article(self.article)
        self.given_a_page("Main")
        self.when_click_link(article.title)
        self.then_i_can_see_article_page(article.title)

    def then_i_will_remove_existing_article(self, id: int):
        """Removes existing article.

        Parameters
        ----------
        id : int
            Article's id.
        """
        delete_link = f"//a[@href='/admin/blog/article/{id}/delete/']"
        self.browser.find_element(By.XPATH, delete_link).click()
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()
        self.then_i_can_see_admin_list_page("Article")
    
    def then_article_is_not_present(self, title: str):
        """Checks if article exists in admin page.

        Parameters
        ----------
        title : str
            Title of article to check.
        """
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.LINK_TEXT, title)

    def then_i_can_see_article_page(self, page_name: str):
        """Checks if article is displayed properly.
        """
        expected_url = f"{self.live_server_url}/articles/{slugify(page_name)}"
        self.assertEqual(expected_url, self.browser.current_url)

        title = self.browser.find_element(By.CSS_SELECTOR, ".article-title")
        publish_date = self.browser.find_element(By.CSS_SELECTOR, ".article-pub-date")
        content = self.browser.find_element(By.CSS_SELECTOR, ".article-content")
        
        current_article = {
            "title": title.text,
            "publish_date": publish_date.text,
            "content": content.text
        }
        expected_article = {
            "title": self.article["title"],
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "content": self.article["content"]
        }
        self.assertDictEqual(current_article, expected_article)
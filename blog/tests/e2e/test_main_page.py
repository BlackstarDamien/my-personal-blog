from selenium.webdriver.common.by import By
from blog.tests.e2e.base import TestBase


class TestMainPage(TestBase):
    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """
        self.create_dummy_articles()
        self.given_a_main_page()
        self.when_vist_this_page("My Personal Blog")
        self.then_i_see_list_of_articles()
    
    def when_vist_this_page(self, page_name: str):
        """Checks if user is on main page

        Args:
            page_name (str): Blog's name.
        """
        self.assertEqual(page_name, self.browser.title)
    
    def then_i_see_list_of_articles(self):
        """Checks if there are any articles displayed on main page.
        """
        articles = self.browser.find_elements(By.CSS_SELECTOR, ".article-link")
        self.assertTrue(len(articles) > 0)
    
    def create_dummy_articles(self):
        """Creates dummy articles.
        """
        test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]
        for article in test_articles:
            self.create_dummy_article(article)

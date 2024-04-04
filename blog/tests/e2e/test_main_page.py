from blog.tests.e2e.base import TestBase
from .pages.main_page import MainPage

class TestMainPage(TestBase):
    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """
        self.create_dummy_articles()
        
        main_page = MainPage(self.browser).navigate()
        articles = main_page.fetch_articles()

        self.assertTrue(len(articles) > 0)

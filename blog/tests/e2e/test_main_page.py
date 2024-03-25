from blog.tests.e2e.base import TestBase
from .pages.main_page import MainPage

class TestMainPage(TestBase):
    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """
        self.create_dummy_articles()
        self.browser.get(self.live_server_url)
        
        main_page = MainPage(self.browser)
        articles = main_page.fetch_articles()

        self.assertTrue(len(articles) > 0)

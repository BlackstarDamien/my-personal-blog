from blog.tests.e2e.base import TestBase
from .pages.main_page import MainPage
from blog.tests.helpers import create_dummy_articles

class TestMainPage(TestBase):
    def setUp(self):
        super().setUp()
        create_dummy_articles(self.test_articles)
        
    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """
        main_page = MainPage(self.browser).navigate()
        articles = main_page.fetch_articles()

        self.assertTrue(len(articles) > 0)

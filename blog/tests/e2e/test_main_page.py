from blog.tests.e2e.base import TestBase
from .pages.main_page import MainPage
from blog.tests.helpers import create_dummy_articles

class TestMainPage(TestBase):
    def setUp(self):
        super().setUp()
        self.articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]

    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """
        create_dummy_articles(self.articles)
        main_page = MainPage(self.browser).navigate()
        articles = main_page.fetch_articles()

        self.assertTrue(len(articles) > 0)

from blog.tests.e2e.base import TestBase
from .pages.main_page import MainPage
from blog.tests.helpers import create_dummy_articles, create_dummy_article

class TestMainPage(TestBase):
    def setUp(self):
        super().setUp()
        # self.articles = create_dummy_articles(self.test_articles)
        for article in self.test_articles:
            create_dummy_article(article)
        
    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """
        # create_dummy_articles(self.test_articles)
        main_page = MainPage(self.browser).navigate()
        articles = main_page.fetch_articles()

        self.assertTrue(len(articles) > 0)

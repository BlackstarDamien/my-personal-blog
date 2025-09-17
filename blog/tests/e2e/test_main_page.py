from blog.tests.e2e.base import TestBase
from .pages.main_page import MainPage
from blog.tests.helpers import create_dummy_articles

class TestMainPage(TestBase):
    @classmethod
    def setUpTestData(cls):
        test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]
        cls.articles = create_dummy_articles(test_articles)
        print(cls.articles[0].objects.all())

    def test_displays_list_of_articles(self):
        """Tests that main page displays list of existing articles.
        """        
        main_page = MainPage(self.browser).navigate()
        articles = main_page.fetch_articles()

        self.assertTrue(len(articles) > 0)

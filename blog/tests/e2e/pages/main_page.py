from typing import List
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .article_page import ArticlePage

class MainPage(BasePage):
    ARTICLES_LOCATOR = (By.CSS_SELECTOR, ".article-link")
    
    def fetch_articles(self) -> List[ArticlePage]:
        """Fetch and return the list of articles.

        Returns
        -------
        List[ArticlePage]
            List of articles from main page.
        """
        articles = []
        for article_locator in self.find(self.ARTICLES_LOCATOR):
            article_page = ArticlePage(self.driver)
            article_page.navigate_to_article(article_locator.text)

        return articles

    def is_article_visible(self, title: str) -> bool:
        """Checks if given article is visible on main page.

        Parameters
        ----------
        title : str
            Checked article's title

        Returns
        -------
        bool
            True if exists, False otherwise.
        """
        all_articles = self.fetch_articles()
        for article in all_articles:
            if article.get_title() == title:
                return True
        
        return False
    
from typing import List
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .about_me_page import AboutMePage

class MainPage(BasePage):
    ARTICLES_LOCATOR = (By.CSS_SELECTOR, ".article-link")
    
    def fetch_articles(self) -> List[str]:
        """Fetch and return the list of articles.

        Returns
        -------
        List[str]
            List of articles from main page.
        """
        return [loc.text for loc in self.find(self.ARTICLES_LOCATOR)]

    def is_article_visible(self, checked_title: str) -> bool:
        """Checks if given article is visible on main page.

        Parameters
        ----------
        checked_title : str
            Checked article's title

        Returns
        -------
        bool
            True if exists, False otherwise.
        """
        all_articles = self.fetch_articles()
        for title in all_articles:
            if title == checked_title:
                return True
        return False
    
    def go_to_about_me_page(self) -> AboutMePage:
        return AboutMePage(self.driver).navigate_to()
    
from typing import List
from .base_page import BasePage


class MainPage(BasePage):
    def fetch_articles(self) -> List[str]:
        """Fetch and return the list of articles.

        Returns
        -------
        List[str]
            List of articles from main page.
        """
        
        return [loc.inner_text() for loc in self.page.locator(".article-link").all()]

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
    
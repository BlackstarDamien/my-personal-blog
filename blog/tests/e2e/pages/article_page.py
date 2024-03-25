from typing import Dict
from selenium.webdriver.common.by import By

from .base_page import BasePage


class ArticlePage(BasePage):
    TITLE_LOCATOR = (By.CSS_SELECTOR, ".article-title")
    DATE_LOCATOR = (By.CSS_SELECTOR, ".article-pub-date")
    CONTENT_LOCATOR = (By.CSS_SELECTOR, ".article-content")

    def get_title(self) -> str:
        """Returns article's title.

        Returns
        -------
        str
            Article's title.
        """
        return self.find(self.TITLE_LOCATOR)[0].text
    
    def get_pub_date(self) -> str:
        """Returns date when article was published.

        Returns
        -------
        str
            Article's published date.
        """
        return self.find(self.DATE_LOCATOR)[0].text
    
    def get_content(self) -> str:
        """Returns content of an article.

        Returns
        -------
        str
            Article's content.
        """
        return self.find(self.CONTENT_LOCATOR)[0].text

    def to_dict(self) -> Dict[str, str]:
        """Converts Article Page to dict object.

        Returns
        -------
        Dict[str, str]
            Converted Article Page.
        """
        return {
            "title": self.get_title(),
            "publish_date": self.get_pub_date(),
            "content": self.get_content()
        }
    
    def navigate_to_article(self, title: str):
        """Opens an article for given title.

        Parameters
        ----------
        title : str
            Article's title
        """
        article_locator = (By.LINK_TEXT, title)
        return self.wait_for(article_locator).click()
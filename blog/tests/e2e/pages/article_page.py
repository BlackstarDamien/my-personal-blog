from typing import Dict, List
from django.template.defaultfilters import slugify
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .base_page import BasePage


class ArticlePage(BasePage):
    PAGE_URI = "/articles/"
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

    def get_all_images(self) -> List[WebElement]:
        """Returns all images from an article.

        Returns
        -------
        List[WebElement]
            List of images
        """
        return self.find((By.TAG_NAME, "img"))

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
    
    def navigate(self, title: str) -> "ArticlePage":
        """Opens an article for given title.

        Parameters
        ----------
        title : str
            Article's title
        """
        page_url = f"{self.base_url}{self.PAGE_URI}"
        self.driver.get(page_url + slugify(title))
        return self
    
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .base_page import BasePage

class MainPage(BasePage):
    ARTICLES_LOCATOR = (By.CSS_SELECTOR, ".article-link")
    
    def fetch_articles(self) -> List[WebElement]:
        """Fetch and return the list of articles.

        Returns
        -------
        List[WebElement]
            List of articles from main page.
        """
        return self.find(self.ARTICLES_LOCATOR)

from typing import Dict
from selenium.webdriver.common.by import By

from .base_page import BasePage


class AboutMePage(BasePage):
    PAGE_LOCATOR = (By.LINK_TEXT, "About Me")
    TITLE_LOCATOR = (By.CSS_SELECTOR, ".about_me-title")
    CONTENT_LOCATOR = (By.CSS_SELECTOR, ".about_me-content")

    def get_title(self) -> str:
        """Returns title of About Me page.

        Returns
        -------
        str
            Title of About Me page.
        """
        return self.find(self.TITLE_LOCATOR)[0].text
        
    def get_content(self) -> str:
        """Returns content of an article.

        Returns
        -------
        str
            Content of About Me page.
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
            "content": self.get_content()
        }
    
    def navigate_to(self) -> "AboutMePage":
        """Opens an About Me page."""
        self.wait_for(self.PAGE_LOCATOR).click()
        return self
    
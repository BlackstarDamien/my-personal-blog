from typing import Dict
from playwright.sync_api import Page


class AboutMePage:
    def __init__(self, page: Page):
        self.page = page
    
    def get_title(self) -> str:
        """Returns title of About Me page.

        Returns
        -------
        str
            Title of About Me page.
        """
        return self.page.locator(".about_me-title").inner_text()
        
    def get_content(self) -> str:
        """Returns content of an article.

        Returns
        -------
        str
            Content of About Me page.
        """
        return self.page.locator(".about_me-content").inner_text()

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
    
    def navigate(self) -> "AboutMePage":
        """Opens an About Me page."""
        page_url = f"{self.page.url}/about-me"
        self.page.goto(page_url)
        return self
    
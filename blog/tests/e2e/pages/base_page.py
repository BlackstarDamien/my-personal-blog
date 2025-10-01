from typing import Optional
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, endpoint: Optional[str] = None) -> "BasePage":
        page_url = self.page.url
        if endpoint:
           page_url = f"{page_url}/{endpoint}" 

        self.page.goto(page_url)
        return self
    
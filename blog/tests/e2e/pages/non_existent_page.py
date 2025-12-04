from .base_page import BasePage
from .main_page import MainPage


class NonExistentPage(BasePage):
    def navigate_to_fake_article(self) -> "NonExistentPage":
        return self.navigate("articles/nonexistent-article")
    
    def navigate_to_fake_static_page(self) -> "NonExistentPage":
        return self.navigate("nonexistent-page")
    
    def get_title(self) -> str:
        return self.page.title()
    
    def get_error_message(self) -> str:
        return self.page.locator(".page-not-found-msg").inner_text()
    
    def click_home_link(self) -> MainPage:
        self.page.locator("text=My Personal Blog").click()
        return MainPage(self.page)
    
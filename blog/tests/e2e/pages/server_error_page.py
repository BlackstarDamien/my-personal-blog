from .base_page import BasePage


class ServerErrorPage(BasePage):
    def navigate_to_error_trigger(self) -> "ServerErrorPage":
        return self.navigate("trigger-500-error")
    
    def get_title(self) -> str:
        return self.page.title()
    
    def get_error_message(self) -> str:
        return self.page.locator(".server-error-msg").inner_text()
    
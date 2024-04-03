from selenium.webdriver.common.by import By

from .base_page import BasePage


class AdminBasePage(BasePage):
    TITLE_LOCATOR = (By.NAME, 'title')
    CONTENT_LOCATOR = (By.NAME, 'content')
    SAVE_BTN_LOCATOR = (By.NAME, "_save")
    DELETE_BTN_LOCATOR = (By.LINK_TEXT, "Delete")
    SUBMIT_BTN_LOCATOR = (By.XPATH, "//input[@type='submit']")
    
    def _enter_title(self, title: str):
        self.find(self.TITLE_LOCATOR)[0].send_keys(title)
    
    def _enter_content(self, content: str):
        self.find(self.CONTENT_LOCATOR)[0].send_keys(content)
    
    def _click_save_button(self):
        self.find(self.SAVE_BTN_LOCATOR)[0].click()


class AdminArticlePage(AdminBasePage):
    ADD_LOCATOR = (By.XPATH, "//a[@href='/admin/blog/article/add/']")
    ARTICLES_LOCATOR = (By.LINK_TEXT, "Articles")

    def add_new_article(self, article: dict):
        self._click_on_add_article()
        self._enter_title(article["title"])
        self._enter_content(article["content"])
        self._click_save_button()
    
    def edit_article(self, title: str, changes: dict):
        self.find(self.ARTICLES_LOCATOR)[0].click()
        self.find((By.LINK_TEXT, title))[0].click()

        for k in changes:
            field_to_change = self.find((By.NAME, k))[0]
            field_to_change.clear()
            field_to_change.send_keys(changes[k])
        
        self._click_save_button()
    
    def delete_article(self, title: str):
        self.find(self.ARTICLES_LOCATOR)[0].click()
        self.find((By.LINK_TEXT, title))[0].click()
        self.find(self.DELETE_BTN_LOCATOR)[0].click()
        self.find(self.SUBMIT_BTN_LOCATOR)[0].click()
    
    def _click_on_add_article(self):
        self.find(self.ADD_LOCATOR)[0].click()


class AdminAboutMePage(AdminBasePage):
    ADD_LOCATOR = (By.XPATH, "//a[@href='/admin/blog/aboutme/add/']")

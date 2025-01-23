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

    def add_new_article(self, article: dict) -> "AdminArticlePage":
        self._click_on_add_article()
        self._enter_title(article["title"])
        self._enter_content(article["content"])
        return self
    
    def attach_images(self, path_to_image: str) -> "AdminArticlePage":
        file_name = self.find((By.ID, "id_image_set-0-name"))[0]
        file_name.send_keys(path_to_image.name)

        file_input = self.find((By.CSS_SELECTOR, "input[type='file']"))[0]
        file_input.send_keys(str(path_to_image))
        
        return self
    
    def save(self):
        self._click_save_button()
    
    def edit_article(self, title: str, changes: dict):
        self.navigate()
        self.find((By.LINK_TEXT, title))[0].click()

        for k in changes:
            field_to_change = self.find((By.NAME, k))[0]
            field_to_change.clear()
            field_to_change.send_keys(changes[k])
        
        self._click_save_button()
    
    def delete_article(self, title: str):
        self.navigate()
        self.find((By.LINK_TEXT, title))[0].click()
        self.find(self.DELETE_BTN_LOCATOR)[0].click()
        self.find(self.SUBMIT_BTN_LOCATOR)[0].click()
    
    def navigate(self) -> "AdminArticlePage":
        """Open articles section in Admin Page.

        Returns
        -------
        AdminArticlePage
            Articles section
        """
        self.find(self.ARTICLES_LOCATOR)[0].click()
        return self
    
    def _click_on_add_article(self):
        self.find(self.ADD_LOCATOR)[0].click()


class AdminAboutMePage(AdminBasePage):
    ADD_LOCATOR = (By.XPATH, "//a[@href='/admin/blog/aboutme/add/']")
    ABOUT_ME_LIST_LOCATOR = (By.LINK_TEXT, "About me")
    ABOUT_ME_LOCATOR = (By.LINK_TEXT, "About Me")

    def fill_content(self, about_me: dict):
        self._click_on_add_about_me()
        self._enter_title(about_me["title"])
        self._enter_content(about_me["content"])
        self._click_save_button()
    
    def edit(self, changes: dict):
        self.navigate()
        self.find(self.ABOUT_ME_LOCATOR)[0].click()

        for k in changes:
            field_to_change = self.find((By.NAME, k))[0]
            field_to_change.clear()
            field_to_change.send_keys(changes[k])
        
        self._click_save_button()

    def navigate(self) -> "AdminAboutMePage":
        """Open About Me section in Admin Page.

        Returns
        -------
        AdminAboutMePage
            About Me section
        """
        self.find(self.ABOUT_ME_LIST_LOCATOR)[0].click()
        return self

    def _click_on_add_about_me(self):
        self.find(self.ADD_LOCATOR)[0].click()

class AdminPage(AdminBasePage):
    def navigate_to_articles(self) -> AdminArticlePage:
        """Redirects to articles section.

        Returns
        -------
        AdminArticlePage
            Articles section
        """
        return AdminArticlePage(self.driver).navigate()
    
    def navigate_to_about_me(self) -> AdminAboutMePage:
        """Redirects to About Me section.

        Returns
        -------
        AdminAboutMePage
            About Me section
        """
        return AdminAboutMePage(self.driver).navigate()
    
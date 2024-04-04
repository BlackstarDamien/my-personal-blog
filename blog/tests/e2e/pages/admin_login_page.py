from selenium.webdriver.common.by import By

from .base_page import BasePage


class AdminLoginPage(BasePage):
    LOGIN_LOCATOR = (By.ID,'id_username')
    PWD_LOCATOR = (By.ID,'id_password')
    SUBMIT_BTN_LOCATOR = (By.XPATH, '//input[@value="Log in"]')

    def navigate(self):
        """Moves user to admin page of given website.
        """
        admin_page_url = self.driver.current_url + "/admin"
        self.driver.get(admin_page_url)

    def login(self, username: str, password: str):
        """Fill login form with given username
        and password

        Parameters
        ----------
        username : str
            Provided username
        password : str
            Provided password
        """
        self.__enter_username(username)
        self.__enter_password(password)
        self.__submit_login_form()

    def __enter_username(self, username: str):
        self.find(self.LOGIN_LOCATOR)[0].send_keys(username)
    
    def __enter_password(self, password: str):
        self.find(self.PWD_LOCATOR)[0].send_keys(password)
    
    def __submit_login_form(self):
        self.find(self.SUBMIT_BTN_LOCATOR)[0].click()
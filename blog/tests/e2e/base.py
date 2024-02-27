from typing import Dict, Optional
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from blog.models import Article


PAGES_TITLES = {
    "admin": lambda name: f"Select {name.lower()} to change | Django site admin",
    "edit_article": lambda name: f"{name} | Change article | Django site admin",
    "edit_about_me": lambda name: f"{name} | Change about me | Django site admin",
    "main": lambda _: "My Personal Blog"
}


class TestBase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.__init_browser()
        self.browser.implicitly_wait(3)

        self.article = {
            "title": "Test Article",
            "content": "Test Content"
        }

        self.admin = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "adm1n"
        }

    def tearDown(self) -> None:
        self.browser.close()
    
    def __init_browser(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

    def given_a_page(self, page_name: str, slug: Optional[str] = None):
        """Goes to app's given page page.
        """
        PAGES = {
            "Main": self.live_server_url,
            "Admin": self.live_server_url + '/admin/',
            "Article": self.live_server_url + f"/articles/{slug}",
            "About me": self.live_server_url + "/about-me"
        }
        self.browser.get(PAGES[page_name])

    def when_click_link(self, link_text: str):
        """Clicks on given link name.

        Args:
            link_text (str): Name of link to click.
        """
        self.browser.find_element(By.LINK_TEXT, link_text).click()
    
    def when_logs_into_admin_page(self):
        """Logs into admin page."""
        username_input = self.browser.find_element(By.ID,'id_username')
        username_input.send_keys(self.admin["username"])
        password_input = self.browser.find_element(By.ID,'id_password')
        password_input.send_keys(self.admin["password"])

        self.browser.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertIn('Site administration', self.browser.title)
    
    def then_i_am_on_the_page(self, page_name: str, element_name: Optional[str] = None):
        """Checks if user is on given page.

        Args:
            page_name (str): Expected page name
            element_name (str): Element expected in page's title, by default None
        """
        expected_name = PAGES_TITLES[page_name](element_name)
        self.assertEqual(expected_name, self.browser.title)
    
    def then_i_will_click_on_add_button(self, button_name: str):
        """Clicks on given add button and redirect to create form.

        Args:
            button_name (str): Name of add button to click.
        """
        lowered_name = button_name.lower() 
        uri_name = lowered_name.replace(" ", "")

        self.browser.refresh()
        self.browser.find_element(By.XPATH, f"//a[@href='/admin/blog/{uri_name}/add/']").click()
        
        self.assertEqual(f"Add {lowered_name} | Django site admin", self.browser.title)

    def create_dummy_articles(self):
        """Creates dummy articles.
        """
        test_articles = [
            {"title": "Test Article 1", "content": "Test Article 1"},
            {"title": "Test Article 2", "content": "Test Article 2"},
            {"title": "Test Article 3", "content": "Test Article 3"}
        ]
        for article in test_articles:
            self.create_dummy_article(article)

    def create_dummy_article(self, article: Dict[str, str]) -> Article:
        """Create dummy article and returns Article's title.

        Returns:
            Article: Instance of created article.
        """
        return Article.objects.create(**article)

    def create_dummy_admin_user(self):
        """Create Admin user for testing purposes.
        """
        User.objects.create_superuser(**self.admin)
    
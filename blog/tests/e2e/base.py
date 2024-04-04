from datetime import datetime
from typing import Dict, Optional
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from blog.models import AboutMe, Article


class TestBase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.__init_browser()
        self.browser.implicitly_wait(3)
        self.browser.get(self.live_server_url)

        self.article = {
            "title": "Test Article",
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
            "content": "Test Content"
        }

        self.about_me = {
            "title": "About Me",
            "content": "Something about me"
        }

        self.admin = {
            "username": "admin",
            "email": "admin@admin.com",
            "password": "adm1n"
        }

    def tearDown(self) -> None:
        self.browser.close()
    
    def __init_browser(self) -> webdriver.Chrome:
        """Initilize webdriver object for Chrome.

        Returns
        -------
        webdriver.Chrome
            Instance of Chrome webdriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

    def given_a_page(self, page_name: str, slug: Optional[str] = None):
        """Goes to app's given page page.

        Parameters
        ----------
        page_name : str
            Name of given page
        slug : Optional[str], optional
            Article's slug, by default None
        """
        PAGES = {
            "Main": "/",
            "Admin": '/admin/',
            "Article": f"/articles/{slug}",
            "About me": "/about-me"
        }
        self.browser.get(self.live_server_url + PAGES[page_name])

    def when_click_link(self, link_text: str):
        """Clicks on given link name.

        Parameters
        ----------
        link_text : str
            Name of link to click.
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
    
    def then_i_can_see_admin_list_page(self, element: str):
        """Checks if user see list of given elements
        in admin panel.

        Parameters
        ----------
        element : str
            Name of elements that should be visible in admin panel.
        """
        current = f"Select {element.lower()} to change | Django site admin"
        self.assertEqual(current, self.browser.title)

    def then_i_can_see_admin_edit_about_me_form(self, title: str):
        """Checks if user see About Me's edit form in admin panel.

        Parameters
        ----------
        title : str
            Title of About Me page.
        """
        current = f"{title} | Change about me | Django site admin"
        self.assertEqual(current, self.browser.title)    

    def then_i_can_see_admin_edit_article_form(self, title: str):
        """Checks if user see article's edit form in admin panel.

        Parameters
        ----------
        title : str
            Title of the Article.
        """
        current = f"{title} | Change article | Django site admin"
        self.assertEqual(current, self.browser.title)

    def then_i_am_on_the_main_page(self):
        """Checks if user is on the main page.
        """
        self.assertEqual("My Personal Blog", self.browser.title)
    
    def then_i_will_click_on_add_button(self, button_name: str):
        """Clicks on given add button and redirect to create form.

        Parameters
        ----------
        button_name : str
            Name of add button to click.
        """
        lowered_name = button_name.lower() 
        uri_name = lowered_name.replace(" ", "")

        self.browser.refresh()
        self.browser.find_element(By.XPATH, f"//a[@href='/admin/blog/{uri_name}/add/']").click()
        
        self.assertEqual(f"Add {lowered_name} | Django site admin", self.browser.title)

    def then_i_will_add_new_page(self, details: Dict[str, str]):
        """Fill add new page form and submit it.

        Parameters
        ----------
        details : Dict[str, str]
            Details of the new page.
        """
        title_field = self.browser.find_element(By.NAME, 'title')
        content_field = self.browser.find_element(By.NAME, 'content')

        title_field.send_keys(details["title"])
        content_field.send_keys(details["content"])
        self.browser.find_element(By.NAME, "_save").click()

    def then_i_will_edit_existing_page(self, changes: Dict[str, str]):
        """Fill edit page form with change for existing page
        and submit them.

        Parameters
        ----------
        changes : Dict[str, str]
            Fields to change with new values.
        """
        for k in changes:
            field_to_change = self.browser.find_element(By.NAME, k)
            field_to_change.clear()
            field_to_change.send_keys(changes[k])
        
        self.browser.find_element(By.NAME, "_save").click()

    def then_page_is_visible_on_admin_page(self, title: str):
        """Checks if page exists in admin page.

        Parameters
        ----------
        title : str
            Title of article to check.
        """
        check = self.browser.find_element(By.LINK_TEXT, title)
        self.assertEqual(check.text, title)
    
    def then_i_can_see_about_me_page(self):
        """Checks if About Me page is displayed properly.
        """
        expected_url = f"{self.live_server_url}/about-me"
        self.assertEqual(expected_url, self.browser.current_url)

        title = self.browser.find_element(By.CSS_SELECTOR, ".about_me-title")
        content = self.browser.find_element(By.CSS_SELECTOR, ".about_me-content")
        
        current_about_me = {
            "title": title.text,
            "content": content.text
        }
        expected_about_me = {
            "title": self.about_me["title"],
            "content": self.about_me["content"]
        }
        self.assertDictEqual(current_about_me, expected_about_me)

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

        Parameters
        ----------
        article : Dict[str, str]
            Data used to initialize Article page's model.

        Returns
        -------
        Article
            Instance of created article.
        """
        return Article.objects.create(**article)

    def create_dummy_about_me_page(self, data: Dict[str, str]) -> AboutMe:
        """Create dummy About Me page.

        Parameters
        ----------
        data : Dict[str, str]
            Data used to initialize About Me page's model.

        Returns
        -------
        AboutMe
            Instance of AboutMe model.
        """
        return AboutMe.objects.create(**data)

    def create_dummy_admin_user(self):
        """Create Admin user for testing purposes.
        """
        User.objects.create_superuser(**self.admin)
    
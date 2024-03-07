from blog.tests.e2e.base import TestBase


class TestNavigation(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.current_article = self.create_dummy_article(self.article)
        self.create_dummy_about_me_page(self.about_me)

    def test_about_me_clicking_on_logo_redirects_to_main_page(self):
        """Tests that when user is on About Me page and when clicks 
        on blog's name, then will be redirected to the main page.
        """
        self.given_a_page("About me")
        self.when_click_link("My Personal Blog")
        self.then_i_am_on_the_main_page()
    
    def test_about_me_clicking_on_posts_tab_redirects_to_main_page(self):
        """Tests that when user is on About Me page and when clicks 
        on 'Posts' tab, then will be redirected to the main page.
        """
        self.given_a_page("About me")
        self.when_click_link("Posts")
        self.then_i_am_on_the_main_page()
    
    def test_article_clicking_on_logo_redirects_to_main_page(self):
        """Tests that when user is on Article page and when clicks 
        on blog's name, then will be redirected to the main page.
        """
        self.given_a_page("Article", self.current_article.slug)
        self.when_click_link("My Personal Blog")
        self.then_i_am_on_the_main_page()
    
    def test_article_clicking_on_posts_tab_redirects_to_main_page(self):
        """Tests that when user is on Article page and when clicks 
        on 'Posts' tab, then will be redirected to the main page.
        """
        self.given_a_page("Article", self.current_article.slug)
        self.when_click_link("Posts")
        self.then_i_am_on_the_main_page()
    
    def test_article_clicking_on_about_me_tab_redirects_to_about_me_page(self):
        """Tests that when user is on Article page and when clicks 
        on 'About Me' tab, then will be redirected to the About Me page.
        """
        self.given_a_page("Article", self.current_article.slug)
        self.when_click_link("About Me")
        self.then_i_can_see_about_me_page()
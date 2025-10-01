from typing import Dict, List
from django.template.defaultfilters import slugify
from playwright.sync_api import Page, Locator


class ArticlePage:
    def __init__(self, page: Page):
        self.page = page

    def get_title(self) -> str:
        """Returns article's title.

        Returns
        -------
        str
            Article's title.
        """
        return self.page.locator(".article-title").inner_text()
    
    def get_pub_date(self) -> str:
        """Returns date when article was published.

        Returns
        -------
        str
            Article's published date.
        """
        return self.page.locator(".article-pub-date").inner_text()
    
    def get_content(self) -> str:
        """Returns content of an article.

        Returns
        -------
        str
            Article's content.
        """
        return self.page.locator(".article-content").text_content().strip()

    def get_all_images(self) -> List[Locator]:
        """Returns all images from an article.

        Returns
        -------
        List[WebElement]
            List of images
        """
        return self.page.locator("img").all()

    def to_dict(self) -> Dict[str, str]:
        """Converts Article Page to dict object.

        Returns
        -------
        Dict[str, str]
            Converted Article Page.
        """
        return {
            "title": self.get_title(),
            "publish_date": self.get_pub_date(),
            "content": self.get_content()
        }
    
    def navigate(self, title: str) -> "ArticlePage":
        """Opens an article for given title.

        Parameters
        ----------
        title : str
            Article's title
        """
        slug = slugify(title)
        page_url = f"{self.page.url}/articles/{slug}"
        self.page.goto(page_url)
        return self
    
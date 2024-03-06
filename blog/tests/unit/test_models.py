from datetime import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from blog.models import Article, AboutMe


class TestArticle(TestCase):
    def setUp(self) -> None:
        self.data = {
            "title": "Test Article",
            "content": "Test Content"
        }
        self.article = self.create_dummy_article(self.data)
    
    def test_should_create_new_article(self):
        """Tests that instance of Article is initialized correctly.
        """
        self.assertEqual(self.article.title, self.data["title"])
        self.assertEqual(self.article.content, self.data["content"])
    
    def test_should_be_represented_by_title(self):
        """Checks if string reprensetation of Article displays
        it's title.
        """
        self.assertEqual(self.data["title"], str(self.article))

    def test_should_generate_slug_when_object_is_saved(self):
        """Checks if initialized Article's instance has
        generated slug based on it's title.
        """
        self.assertEqual(self.article.slug, "test-article")
    
    def test_throws_error_when_slug_not_unique(self):
        """Ensures that it's not possible to create an Article
        with the same data and slug.
        """
        with self.assertRaises(IntegrityError):
            self.create_dummy_article(self.data)
    
    def test_should_calculate_url_for_given_object(self):
        """Checks if get_absolute_url() returns correct
        URL to an Article page.
        """
        self.assertEqual(f"/articles/{self.article.slug}", 
                         self.article.get_absolute_url())
    
    def test_should_set_publish_date_once_its_created(self):
        """Checks if initizalized Article's object has correct value of
        publish_date.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        expected_date = self.article.publish_date.strftime("%Y-%m-%d")
        self.assertEqual(expected_date, current_date)

    def create_dummy_article(self, data) -> Article:
        """Initialize instance of Article based on dummy data.

        Parameters
        ----------
        data : _type_
            Dummy data used to create Article's object.

        Returns
        -------
        Article
            Dummy Article.
        """
        return Article.objects.create(**data)


class TestAboutMe(TestCase):
    def setUp(self) -> None:
        self.data = {
            "title": "About Me",
            "content": "Something about me"
        }
        self.about_me = AboutMe.objects.create(**self.data)
    
    def test_should_create_new_about_me_instance(self):
        """Checks if AboutMe object is initialized correctly.
        """
        self.assertEqual(self.about_me.title, self.data["title"])
        self.assertEqual(self.about_me.content, self.data["content"])
    
    def test_save_not_create_new_instance(self):
        """Ensures that there can be only one instance of AboutMe
        created.
        """
        data = {
            "title": "About Me",
            "content": "Something new about me"
        }
        AboutMe.objects.create(**data)
        about_me_count = AboutMe.objects.all().count()
        about_me_updated = AboutMe.objects.first()

        self.assertEqual(about_me_count, 1)
        self.assertEqual(about_me_updated.content, data["content"])

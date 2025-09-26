from django.test import TestCase
from blog.models import AboutMe
from blog.tests.helpers import (
    create_dummy_about_me
)


class TestAboutMe(TestCase):
    def setUp(self) -> None:
        self.data = {
            "title": "About Me",
            "content": "Something about me"
        }
        self.about_me = create_dummy_about_me(self.data)
    
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
        create_dummy_about_me(data)
        about_me_count = AboutMe.objects.all().count()
        about_me_updated = AboutMe.objects.first()

        self.assertEqual(about_me_count, 1)
        self.assertEqual(about_me_updated.content, data["content"])

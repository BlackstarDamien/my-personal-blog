from django.test import TestCase
from blog.tests.helpers import (
    create_dummy_image,
    create_dummy_article
)


class TestImage(TestCase):
    def setUp(self):
        self.article = create_dummy_article(
            {
                "title": "Test Article",
                "content": "Test Content"
            }
        )
    
    def test_should_create_new_instance(self):
        """Checks if object model for Image is created properly.
        """
        test_image_name = "black-cat.jpg"
        image = create_dummy_image(test_image_name)
        self.assertEqual(image.name, test_image_name)
        self.assertEqual(str(image.url).split("/")[-1], test_image_name)

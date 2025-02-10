import markdown
import unittest
from blog.extensions import DjangoMediaImageExtension
from django.conf import settings


class TestDjangoMediaImage(unittest.TestCase):
    def test_img_tag_with_local_source(self):
        """Tests that path to local file can be parsed correctly."""
        img_url_map = {
            "black-cat.jpg": "/images/black-cat.jpg"
        }
        extension = DjangoMediaImageExtension(img_url_map=img_url_map)
        md = markdown.Markdown(extensions=[extension])

        text = """![](black-cat.jpg)"""
        result = md.convert(text)

        image_path = settings.MEDIA_URL + "/images/black-cat.jpg"
        expected = f'<p><img alt="" src="{image_path}" /></p>'
        self.assertEqual(result, expected)

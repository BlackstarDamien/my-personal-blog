import markdown
import unittest
from blog.extensions import DjangoMediaImageExtension


class TestDjangoMediaImage(unittest.TestCase):
    def test_img_tag_with_local_source(self):
        """Tests that path to local file can be parsed correctly."""
        extension = DjangoMediaImageExtension()
        md = markdown.Markdown(extensions=[extension])

        text = """![](images/black-cat.jpg)"""
        result = md.convert(text)

        expected = '<p><img alt="" src="{{ MEDIA_URL }}/images/black-cat.jpg" /></p>'
        self.assertEqual(result, expected)

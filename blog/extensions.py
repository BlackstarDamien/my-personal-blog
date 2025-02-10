from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from django.conf import settings
from typing import Dict


class DjangoMediaImageTreeProcessor(Treeprocessor):
    def run(self, root):
        """Extension logic"""
        images = root.iter("img")
        img_url_map = self.config["img_url_map"]
        for img in images:
            if img.get("src") and img.get("src") in img_url_map:
                img_url = img_url_map[img.get("src")]
                img.set("src", settings.MEDIA_URL + img_url)


class DjangoMediaImageExtension(Extension):
    def __init__(self, **kwargs):
        """Initialize configuration"""
        self.config = {
            "img_url_map": [{}, "URLs for every defined image"]
        }
        super(DjangoMediaImageExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        """Include DjangoMediaImageExtension into Markdown instance."""
        md.registerExtension(self)
        extension = DjangoMediaImageTreeProcessor(md)
        extension.config = self.getConfigs()
        md.treeprocessors.register(
            extension,
            "django_media_image_pattern",
            -1
        )

def makeExtension(**kwargs):
    return DjangoMediaImageExtension(**kwargs)

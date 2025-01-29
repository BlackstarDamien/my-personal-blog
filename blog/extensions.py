from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class DjangoMediaImageTreeProcessor(Treeprocessor):
    def run(self, root):
        """Extension logic"""
        images = root.iter("img")
        for img in images:
            if img.get("src"):
                img.set("src", "{{ MEDIA_URL }}/" + img.get("src"))


class DjangoMediaImageExtension(Extension):
    def __init__(self, **kwargs):
        """Initialize configuration"""
        super(DjangoMediaImageExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        """Include DjangoMediaImageExtension into Markdown instance."""
        md.registerExtension(self)
        extension = DjangoMediaImageTreeProcessor(md)
        md.treeprocessors.register(
            extension,
            "django_media_image_pattern",
            -1
        )

def makeExtension(**kwargs):
    return DjangoMediaImageExtension(**kwargs)

from django.db import models
from django.template.defaultfilters import slugify


class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    slug = models.SlugField(null=False)

    def __str__(self) -> str:
        """Generates string representation of model.

        Returns:
            str: String representation of Article.
        """
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
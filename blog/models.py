from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self) -> str:
        """Generates string representation of model.

        Returns:
            str: String representation of Article.
        """
        return self.title

    def get_absolute_url(self) -> str:
        """Get full url to given Article.

        Returns:
            str: Absolute url of given Article's instance.
        """
        return reverse("article_page", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Saves given Article's instance into database.
        """
        if not self.slug or self.slug == '':
            self.slug = slugify(self.title)    
        return super().save(*args, **kwargs)

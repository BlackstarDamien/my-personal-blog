from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Page(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    
    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        """Generates string representation of model.

        Returns:
            str: String representation of Article.
        """
        return self.title

class Article(Page):
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)

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


class AboutMe(Page):
    def get_absolute_url(self) -> str:
        """Get full url to About Me Page.

        Returns:
            str: Absolute url of About Me page.
        """
        return reverse("about_me_page")

    def save(self, *args, **kwargs):
        """Saves given AboutMe instace into database.
        When a single instance exists, it updates existing
        instance.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        return super().save(*args, **kwargs)
    
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

        Returns
        -------
        str
            String representation of Article.
        """
        return self.title

class Article(Page):
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)

    def get_absolute_url(self) -> str:
        """Get full URL to given Article.

        Returns
        -------
        str
            Absolute URL of given Article's instance.
        """
        return reverse("article_page", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs) -> "Article":
        """Saves given Article's instance into database.

        Returns
        -------
        Article
            Created or updated instance of Article.
        """
        if not self.slug or self.slug == '':
            self.slug = slugify(self.title)    
        return super().save(*args, **kwargs)


class AboutMe(Page):
    class Meta:
        verbose_name_plural = "about me"

    def get_absolute_url(self) -> str:
        """Get full URL to About Me Page.

        Returns
        -------
        str
            Absolute URL of About Me page.
        """
        return reverse("about_me_page")

    def save(self, *args, **kwargs) -> "AboutMe":
        """Saves given AboutMe instace into database.
        When a single instance exists, it updates existing
        instance.

        Returns
        -------
        AboutMe
            Created or updated instance of AboutMe.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        return super().save(*args, **kwargs)

class Image(models.Model):
    name = models.CharField(max_length=120)
    url = models.ImageField(upload_to="images", null=True, blank=True)
    article = models.ForeignKey(Article, related_name="images", on_delete=models.CASCADE)

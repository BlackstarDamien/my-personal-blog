from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()

    def __str__(self) -> str:
        """Generates string representation of model.

        Returns:
            str: String representation of Article.
        """
        return self.title
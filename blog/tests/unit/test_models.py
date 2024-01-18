from blog.models import Article
from django.test import TestCase


class TestArticle(TestCase):
    def test_should_create_new_article(self):
        data = {
            "title": "Test Article",
            "content": "Test Content"
        }
        Article.objects.create(**data)
        article = Article.objects.get(title=data["title"])
        self.assertEquals(article.title, data["title"])
        self.assertEquals(article.content, data["content"])
        
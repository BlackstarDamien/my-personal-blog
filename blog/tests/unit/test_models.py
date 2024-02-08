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
        self.assertEqual(article.title, data["title"])
        self.assertEqual(article.content, data["content"])
    
    def test_should_be_represented_by_title(self):
        data = {
            "title": "Test Article",
            "content": "Test Content"
        }
        article = Article(**data)
        self.assertEqual(data["title"], str(article))

    def test_should_generate_slug_when_object_is_saved(self):
        data = {
            "title": "Test Article",
            "content": "Test Content"
        }
        Article.objects.create(**data)
        article = Article.objects.get(title=data["title"])
        self.assertEqual(article.slug, "test-article")
    
    def test_should_calculate_url_for_given_object(self):
        data = {
            "title": "Test Article",
            "content": "Test Content"
        }
        Article.objects.create(**data)
        article = Article.objects.get(title=data["title"])
        self.assertEqual(f"/articles/{article.slug}", article.get_absolute_url())

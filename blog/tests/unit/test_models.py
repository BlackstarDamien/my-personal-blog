from datetime import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from blog.models import Article


class TestArticle(TestCase):
    def setUp(self) -> None:
        self.data = {
            "title": "Test Article",
            "content": "Test Content"
        }
        Article.objects.create(**self.data)
        self.article = Article.objects.get(title=self.data["title"])
    
    def test_should_create_new_article(self):
        self.assertEqual(self.article.title, self.data["title"])
        self.assertEqual(self.article.content, self.data["content"])
    
    def test_should_be_represented_by_title(self):
        self.assertEqual(self.data["title"], str(self.article))

    def test_should_generate_slug_when_object_is_saved(self):
        self.assertEqual(self.article.slug, "test-article")
    
    def test_throws_error_when_slug_not_unique(self):
        with self.assertRaises(IntegrityError):
            Article.objects.create(title="Test Article", 
                                   content="New content")
    
    def test_should_calculate_url_for_given_object(self):
        self.assertEqual(f"/articles/{self.article.slug}", 
                         self.article.get_absolute_url())
    
    def test_should_set_publish_date_once_its_created(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        expected_date = self.article.publish_date.strftime("%Y-%m-%d")
        self.assertEqual(expected_date, current_date)

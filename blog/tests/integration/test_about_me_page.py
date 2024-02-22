from django.test import TestCase
from blog.models import AboutMe


class TestAboutMePageView(TestCase):
    def setUp(self) -> None:
        self.about_me = AboutMe.objects.create(
            title="About Me",
            content="Short text about me."
        )
        self.about_me_url = self.about_me.get_absolute_url()
    
    def test_about_me_page_returns_correct_html(self):
        """Test that about me page returns proper html file.
        """
        response = self.client.get(self.about_me_url)
        self.assertTemplateUsed(response, 'about_me.html')

    def test_about_me_page_receives_proper_context_data(self):
        """Tests that about me page returns proper data in context.
        """
        response = self.client.get(self.about_me_url)
        self.assertEqual(self.about_me, response.context["about_me"])
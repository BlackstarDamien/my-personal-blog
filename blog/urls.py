from django.urls import path

from blog.views import main_page, article_page

urlpatterns = [
    path("", main_page, name="index"),
    path("articles/<slug:slug>", article_page, name="article_page")
]
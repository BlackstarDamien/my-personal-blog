from django.urls import path
from django.conf.urls import handler404, handler500

from blog.views import about_me_page, article_page, main_page

urlpatterns = [
    path("", main_page, name="index"),
    path("about-me", about_me_page, name="about_me_page"),
    path("articles/<slug:slug>", article_page, name="article_page")
]

handler404 = "blog.views.page_not_found_view"
handler500 = "blog.views.server_error_view"

from django.urls import path

from blog.views import main_page

urlpatterns = [
    path("", main_page, name="index")
]
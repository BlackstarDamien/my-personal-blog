from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from blog.models import Article, AboutMe


def main_page(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, 'index.html', context)

def article_page(request: HttpRequest, slug: str) -> HttpResponse:
    article = Article.objects.get(slug=slug)
    context = {"article": article}
    return render(request, 'article.html', context)

def about_me_page(request: HttpRequest) -> HttpResponse:
    about_me = AboutMe.objects.first()
    context = {"about_me": about_me}
    return render(request, 'about_me.html', context)

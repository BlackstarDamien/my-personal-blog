from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from blog.models import Article


def main_page(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, 'index.html', context)

def article_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'article.html')
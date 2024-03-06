from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from blog.models import Article, AboutMe


def main_page(request: HttpRequest) -> HttpResponse:
    """Renders main page with list of Articles.

    Parameters
    ----------
    request : HttpRequest
        HTTP request to main page.

    Returns
    -------
    HttpResponse
        Rendered main page.
    """
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, 'index.html', context)

def article_page(request: HttpRequest, slug: str) -> HttpResponse:
    """Renders Article's page with proper data.

    Parameters
    ----------
    request : HttpRequest
        HTTP request to given Article's page.
    slug : str
        Article's slug.

    Returns
    -------
    HttpResponse
        Rendered Article page.
    """
    article = Article.objects.get(slug=slug)
    context = {"article": article}
    return render(request, 'article.html', context)

def about_me_page(request: HttpRequest) -> HttpResponse:
    """Renders About Me page with proper data.

    Parameters
    ----------
    request : HttpRequest
        HTTP request to given About Me page.

    Returns
    -------
    HttpResponse
        Rendered About Me page.
    """
    about_me = AboutMe.objects.first()
    context = {"about_me": about_me}
    return render(request, 'about_me.html', context)

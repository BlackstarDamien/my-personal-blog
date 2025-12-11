from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
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
    article = get_object_or_404(Article, slug=slug)
    img_url_map = {x.name: str(x.url) for x in article.images.all()}
    context = {"article": article, "img_url_map": img_url_map}
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

def page_not_found_view(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Renders custom 404 page.

    Parameters
    ----------
    request : HttpRequest
        HTTP request that resulted in 404.
    exception : Exception
        Exception that triggered the 404.

    Returns
    -------
    HttpResponse
        Rendered 404 page.
    """
    return render(request, '404.html', status=404)

def server_error_view(request: HttpRequest) -> HttpResponse:
    """Renders custom 500 page.

    Parameters
    ----------
    request : HttpRequest
        HTTP request that resulted in 500.

    Returns
    -------
    HttpResponse
        Rendered 500 page.
    """
    return render(request, '500.html', status=500)

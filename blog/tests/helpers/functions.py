from io import BytesIO
from PIL import Image as PILImage
from typing import List
from blog.models import AboutMe, Article, Image
from django.core.files.images import ImageFile


def create_dummy_about_me(data: dict) -> AboutMe:
    """Initialize instance of AboutMe based on dummy data.

    Parameters
    ----------
    data : dict
        Dummy data used to create AboutMe's object.

    Returns
    -------
    AboutMe
        Dummy AboutMe object.
    """
    return AboutMe.objects.create(**data)

def create_dummy_articles(test_articles: List[dict]):
    """Creates dummy articles.
    """
    for article in test_articles:
        create_dummy_article(article)
    
    # TODO: Remove
    print(Article.objects.all())

def create_dummy_article(data: dict) -> Article:
    """Initialize instance of Article based on dummy data.

    Parameters
    ----------
    data : dict
        Dummy data used to create Article's object.

    Returns
    -------
    Article
        Dummy Article object.
    """
    return Article.objects.create(**data)
   

def create_dummy_image(file_name: str) -> Image:
    """Initialize instance of Image model.

    Parameters
    ----------
    file_name : str
        Name of dummy Image file.

    Returns
    -------
    Image
        Dummy Image object.
    """
    test_image_content = __create_temp_img_content()
    image_file = ImageFile(
            file=test_image_content,
            name=file_name
    )

    article_image = Image(
        name=file_name,
        url=image_file,
    )

    return article_image

def __create_temp_img_content() -> BytesIO:
    temp_img = BytesIO()
    image = PILImage.new(
        mode="RGB",
        size=(200, 200),
        color=(255, 0, 0, 0)
    )
    image.save(temp_img, "jpeg")
    temp_img.seek(0)
    return temp_img

def create_article_with_image(article: dict, filename: str):
    md_article = create_dummy_article(article)
    articles_image = create_dummy_image(filename)
    bind_image_with_article(articles_image, md_article)

def bind_image_with_article(image: Image, article: Article) -> Image:
    image.article = article
    image.save()
    return image

import markdown
from django import template
from django.utils.html import mark_safe
from blog.extensions import DjangoMediaImageExtension

register = template.Library()


@register.filter
def md_to_html(value, img_url_map):
    extension = DjangoMediaImageExtension(img_url_map=img_url_map)
    md_converter = markdown.Markdown(extensions=[extension])
    converted_content = md_converter.convert(value)
    return mark_safe(converted_content)

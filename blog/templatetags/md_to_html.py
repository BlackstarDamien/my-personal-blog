import markdown
from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def md_to_html(value):
    md_converter = markdown.Markdown()
    converted_content = md_converter.convert(value)
    return mark_safe(converted_content)

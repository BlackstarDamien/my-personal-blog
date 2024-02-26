from django.contrib import admin
from blog.models import AboutMe, Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ["title", "content"]

admin.site.register(AboutMe)
admin.site.register(Article, ArticleAdmin)

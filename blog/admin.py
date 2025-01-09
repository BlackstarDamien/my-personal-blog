from django.contrib import admin
from blog.models import AboutMe, Article, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    fields = ["title", "content"]
    inlines = [ImageInline]

admin.site.register(AboutMe)
admin.site.register(Article, ArticleAdmin)

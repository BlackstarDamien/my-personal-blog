# Generated by Django 5.0.1 on 2024-02-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_article_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]

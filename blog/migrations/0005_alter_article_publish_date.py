# Generated by Django 5.0.1 on 2024-02-12 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_article_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

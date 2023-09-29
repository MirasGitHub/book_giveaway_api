# Generated by Django 4.2.5 on 2023-09-28 12:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0003_book_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='interested_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='is_offered',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 4.2.5 on 2023-09-28 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_remove_book_is_offered'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_offered',
            field=models.BooleanField(default=False),
        ),
    ]

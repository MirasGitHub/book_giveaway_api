# Generated by Django 4.2.5 on 2023-09-28 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_book_interested_users_book_is_offered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='is_offered',
            field=models.BooleanField(default=True),
        ),
    ]

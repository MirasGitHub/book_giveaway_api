# Generated by Django 4.2.5 on 2023-09-30 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('comment', models.TextField(blank=True, null=True)),
                ('location', models.CharField(max_length=200)),
                ('is_available', models.BooleanField(default=True)),
                ('is_offered', models.BooleanField(default=False)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.condition')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.genre')),
                ('interested_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

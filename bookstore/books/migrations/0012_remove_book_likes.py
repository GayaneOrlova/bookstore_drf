# Generated by Django 4.2.5 on 2023-09-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_book_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='likes',
        ),
    ]
# Generated by Django 4.2.5 on 2023-10-11 18:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0059_remove_comment_updated_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookLike',
            new_name='BookFavorite',
        ),
    ]
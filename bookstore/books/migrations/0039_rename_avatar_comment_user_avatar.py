# Generated by Django 4.2.5 on 2023-09-27 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0038_comment_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='avatar',
            new_name='user_avatar',
        ),
    ]

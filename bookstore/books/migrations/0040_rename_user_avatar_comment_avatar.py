# Generated by Django 4.2.5 on 2023-09-27 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0039_rename_avatar_comment_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_avatar',
            new_name='avatar',
        ),
    ]

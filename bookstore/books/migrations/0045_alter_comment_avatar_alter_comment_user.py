# Generated by Django 4.2.5 on 2023-09-27 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0011_remove_customuser_bio_alter_customuser_username'),
        ('books', '0044_alter_comment_avatar_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='avatar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.avatar'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
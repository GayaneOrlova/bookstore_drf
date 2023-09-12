# Generated by Django 4.2.5 on 2023-09-12 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0007_alter_book_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='likes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]

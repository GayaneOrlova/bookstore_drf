# Generated by Django 4.2.5 on 2023-10-11 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0058_book_bestseller_book_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='updated_at',
        ),
    ]
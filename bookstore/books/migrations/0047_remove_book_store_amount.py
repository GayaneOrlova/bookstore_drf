# Generated by Django 4.2.5 on 2023-09-28 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0046_book_store_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='store_amount',
        ),
    ]

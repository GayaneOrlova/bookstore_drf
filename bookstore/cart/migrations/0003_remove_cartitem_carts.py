# Generated by Django 4.2.5 on 2023-09-28 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_cart_item_cart_items_remove_cartitem_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='carts',
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-27 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cart_bought'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='carts',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cart.cart'),
            preserve_default=False,
        ),
    ]

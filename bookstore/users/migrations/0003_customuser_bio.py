# Generated by Django 4.2.5 on 2023-09-18 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_username_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

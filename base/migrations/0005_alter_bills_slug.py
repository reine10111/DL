# Generated by Django 4.2.7 on 2023-11-24 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_bills_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]

# Generated by Django 5.0 on 2023-12-13 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_delete_remark'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Events',
        ),
    ]
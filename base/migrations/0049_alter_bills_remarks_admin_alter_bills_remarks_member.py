# Generated by Django 4.2.7 on 2023-12-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_remove_submission_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='remarks_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bills',
            name='remarks_member',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-11 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0046_admin_first_name_admin_last_name_member_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
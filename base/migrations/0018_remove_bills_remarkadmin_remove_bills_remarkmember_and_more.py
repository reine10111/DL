# Generated by Django 4.2.7 on 2023-11-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_remove_bills_remarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bills',
            name='remarkAdmin',
        ),
        migrations.RemoveField(
            model_name='bills',
            name='remarkMember',
        ),
        migrations.AddField(
            model_name='bills',
            name='remarks',
            field=models.CharField(default='', max_length=255),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-30 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_submission_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default='P', max_length=255),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_remove_submission_files_delete_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='text',
        ),
        migrations.AddField(
            model_name='submission',
            name='proof',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]

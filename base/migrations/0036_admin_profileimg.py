# Generated by Django 4.2.7 on 2023-12-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_remove_admin_profile_remove_member_profile_admin_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='profileimg',
            field=models.ImageField(default='blank-profile.jpg', upload_to='profile_images'),
        ),
    ]

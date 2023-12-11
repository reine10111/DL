# Generated by Django 4.2.7 on 2023-12-10 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0044_groupcontrib_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcontrib',
            name='selected_user_ids',
            field=models.ManyToManyField(related_name='selected_user_ids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='groupcontrib',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='groupcontrib',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
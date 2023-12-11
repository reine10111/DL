# Generated by Django 4.2.7 on 2023-11-26 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_bills_remarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='PysicalSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(null=True)),
                ('bills', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.bills')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.2 on 2023-11-01 08:07

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_story'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='b2StorageFile',
            field=models.FileField(blank=True, upload_to=api.models.upload_to_story, verbose_name='B2 Storage File'),
        ),
    ]
# Generated by Django 4.2 on 2024-05-07 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_homepagecard_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagecard',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
# Generated by Django 4.2 on 2024-04-20 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_hopmepagerow_homepagecard_row'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagecard',
            name='menu',
        ),
    ]

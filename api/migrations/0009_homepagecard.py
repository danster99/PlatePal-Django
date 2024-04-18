# Generated by Django 4.2 on 2024-04-09 07:13

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('size', models.CharField(choices=[('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')])),
                ('b2StorageFile', models.FileField(blank=True, upload_to=api.models.upload_to_card, verbose_name='B2 Storage File')),
                ('text', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('links_to', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('menu', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='api.menu')),
            ],
        ),
    ]
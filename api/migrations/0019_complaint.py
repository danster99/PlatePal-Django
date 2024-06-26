# Generated by Django 4.2 on 2024-05-19 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.menu')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.table')),
            ],
        ),
    ]

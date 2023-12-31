# Generated by Django 4.2.1 on 2023-06-15 10:53

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('isFood', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('features', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Core'), (2, 'Feedback'), (3, 'Statistics'), (4, 'In-App Interaction'), (5, 'AR'), (6, 'Dynamic Pricing')], max_length=10)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField()),
                ('b2StorageFile', models.FileField(blank=True, upload_to='uploads', verbose_name='B2 Storage File')),
                ('alergens', models.TextField(blank=True, null=True)),
                ('isVegan', models.BooleanField(default=False)),
                ('isDairyFree', models.BooleanField(default=False)),
                ('isGlutenFree', models.BooleanField(default=False)),
                ('spiceLvl', models.IntegerField(default=0)),
                ('nutriValues', models.JSONField(blank=True, null=True)),
                ('clicks24h', models.IntegerField(default=0)),
                ('clicks7d', models.IntegerField(default=0)),
                ('clicks30d', models.IntegerField(default=0)),
                ('isAvailable', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.menu'),
        ),
    ]

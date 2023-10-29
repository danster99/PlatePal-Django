# Generated by Django 4.2 on 2023-10-29 19:38

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_item_b2storagefile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='features',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=6),
        ),
        migrations.AddField(
            model_name='item',
            name='aditives',
            field=models.TextField(blank=True, null=True),
        ),

        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('seats', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card'), ('PayPal', 'PayPal'), ('ApplePay', 'ApplePay'), ('GooglePay', 'GooglePay')])),
                ('tip', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.restaurant')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.table')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Checkout', 'Checkout'), ('Closed', 'Closed')], default='Open')),
                ('table', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.table')),
            ],
        ),
    ]
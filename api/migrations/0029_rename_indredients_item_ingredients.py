# Generated by Django 4.2 on 2024-06-12 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_item_indredients_item_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='indredients',
            new_name='ingredients',
        ),
    ]
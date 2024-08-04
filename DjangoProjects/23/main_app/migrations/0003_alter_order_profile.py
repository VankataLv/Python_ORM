# Generated by Django 5.0.4 on 2024-07-30 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_product_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main_app.profile'),
        ),
    ]
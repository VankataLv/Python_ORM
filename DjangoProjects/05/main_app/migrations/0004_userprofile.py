# Generated by Django 5.0.4 on 2024-06-23 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('username', models.CharField(max_length=65, unique=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(default='students@softuni.bg', max_length=254, unique=True)),
                ('bio', models.TextField(max_length=120)),
                ('profile_image_url', models.URLField()),
            ],
        ),
    ]

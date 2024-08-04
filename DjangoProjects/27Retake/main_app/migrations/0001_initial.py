# Generated by Django 5.0.4 on 2024-08-01 04:58

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TennisPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(5)])),
                ('birth_date', models.DateField()),
                ('country', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('ranking', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(300)])),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('location', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('prize_money', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('surface_type', models.CharField(choices=[('Not Selected', 'Not Selected'), ('Clay', 'Clay'), ('Grass', 'Grass'), ('Hard Court', 'Hard Court')], default='Not Selected', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=100)),
                ('summary', models.TextField(validators=[django.core.validators.MinLengthValidator(5)])),
                ('date_played', models.DateTimeField()),
                ('players', models.ManyToManyField(to='main_app.tennisplayer')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches_winner', to='main_app.tennisplayer')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_tournament', to='main_app.tournament')),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
    ]

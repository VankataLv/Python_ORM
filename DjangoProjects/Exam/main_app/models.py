from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models
from main_app.managers import AstronautManager


# Create your models here.
class Astronaut(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    phone_number = models.CharField(max_length=15, unique=True,
                                    validators=[RegexValidator(regex=r'^\d+$')])
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=StatusChoices.choices, max_length=9, default="Planned")
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='ship_missions')
    astronauts = models.ManyToManyField(Astronaut, related_name='crew_mission')
    commander = models.ForeignKey(Astronaut, null=True, on_delete=models.SET_NULL, related_name='commander_mission')

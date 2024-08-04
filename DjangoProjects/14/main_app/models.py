from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
# ------------ 7 ---------------------
class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, 'Available'),
                            (False, 'Not Available'))
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self) -> int:
        cur_age = date.today() - self.birth_date
        return cur_age.days // 365

class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


# ------------ 2 + 4 ---------------------
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    SPECIALTY_CHOICES = (
        ("Mammals", "Mammals"),
        ("Birds", "Birds"),
        ("Reptiles", "Reptiles"),
        ("Others", "Others"),
    )

    specialty = models.CharField(max_length=10, choices=SPECIALTY_CHOICES)
    managed_animals = models.ManyToManyField(Animal, related_name='animal')

    # ------------ 4 ---------------------
    def clean(self):
        choices = [choices[0] for choices in self.SPECIALTY_CHOICES]
        if self.specialty not in choices:
            raise ValidationError('Specialty must be a valid choice.')


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

# ------------ 3 ---------------------
class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self) -> str:
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self) -> str:
        ENDANGERED_SPECIES = {"Cross River Gorilla", "Orangutan", "Green Turtle"}

        if self.species in ENDANGERED_SPECIES:
            return f"{self.species} is at risk!"
        else:
            return f"{self.species} is not at risk."







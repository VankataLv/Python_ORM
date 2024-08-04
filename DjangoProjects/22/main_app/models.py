from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.mixins import AwardedMixin, UpdatedMixin
from main_app.managers import DirectorManager


# Create your models here.
class BaseClass(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')


class Director(BaseClass):
    years_of_experience = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(BaseClass, AwardedMixin, UpdatedMixin):
    pass


class Movie(AwardedMixin, UpdatedMixin):
    class MoviesGenre(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=6, choices=MoviesGenre.choices, default='Other')
    rating = models.DecimalField(default=0.0, max_digits=3, decimal_places=1, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(10.0),
    ])
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='director_movies')
    starring_actor = models.ForeignKey(Actor, null=True, on_delete=models.SET_NULL, related_name='starring_movies')
    actors = models.ManyToManyField(Actor, related_name='actors_movies')

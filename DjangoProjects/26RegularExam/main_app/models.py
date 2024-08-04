from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.manager import AuthorManager


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[MinValueValidator(1900),
                                                         MaxValueValidator(2005)])
    website = models.URLField(blank=True, null=True)

    objects = AuthorManager()


class Article(models.Model):
    class ArticlesCategories(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    category = models.CharField(max_length=10,
                                choices=ArticlesCategories.choices,
                                default='Technology')
    authors = models.ManyToManyField(Author)
    published_on = models.DateTimeField(auto_now_add=True, editable=False)


class Review(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.FloatField(validators=[MinValueValidator(1.0),
                                           MinValueValidator(5.0)])
    author = models.ForeignKey(Author, related_name='author_reviews', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='article_reviews', on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True, editable=False)

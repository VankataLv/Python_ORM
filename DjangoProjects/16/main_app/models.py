from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Index


# Create your models here.
class ReviewMixin(models.Model):
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])

    class Meta:
        abstract = True
        ordering = ['-rating']

class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Name must be at least 2 characters long."),
            MaxLengthValidator(
                limit_value=100,
                message="Name cannot exceed 100 characters."
            ),
        ])

    location = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Location must be at least 2 characters long."),
            MaxLengthValidator(
                limit_value=200,
                message="Location cannot exceed 200 characters."
            ),
        ])

    description = models.TextField(null=True, blank=True, )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0.00,
                message="Rating must be at least 0.00."),
            MaxValueValidator(
                limit_value=5.00,
                message="Rating cannot exceed 5.00."
            ),
        ])


# ----- 2 -----
def validate_menu_categories(value):
    ALLOWED_CATEGORIES = ["Appetizers", "Main Course", "Desserts"]

    for category in ALLOWED_CATEGORIES:
        if category.lower() not in value.lower():
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", '
                                  '"Desserts".')


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)


# ----- 3 -----


class RestaurantReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    # review_content = models.TextField()
    # rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])

    class Meta(ReviewMixin.Meta):
        # ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant']
        abstract = True


# ----- 4 -----
class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'
        unique_together = ['reviewer_name', 'restaurant']


# ----- 5 -----

class MenuReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(to=Menu, on_delete=models.CASCADE)
    # review_content = models.TextField()
    # rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])

    class Meta(ReviewMixin.Meta):
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ['reviewer_name', 'menu']
        indexes = [Index(fields=['menu', ], name='main_app_menu_review_menu_id')]

# ----- 6 -----

from django.db import models


class AwardedMixin(models.Model):
    class Meta:
        abstract=True

    is_awarded = models.BooleanField(default=False)


class UpdatedMixin(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(auto_now=True)
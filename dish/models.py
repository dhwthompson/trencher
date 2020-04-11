from django.contrib.postgres.fields import ArrayField
from django.db import models


class Dish(models.Model):
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dishes"

    name = models.CharField(max_length=200)
    ingredients = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    def __str__(self):
        return self.name

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Dish(models.Model):
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dishes"

    name = models.CharField(max_length=200)
    recipe_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class IngredientSection(models.TextChoices):
    """Identify different types of ingredients.

    This model lets us pull certain ingredients apart into particular sections,
    mostly based on which part of the store they're in.
    """

    MEAT = "meat", "Meat counter"
    VEG = "veg", "Fruit and veg"


class Ingredient(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=200, unique=True)
    dishes = models.ManyToManyField(Dish, related_name="ingredients")
    section = models.CharField(
        max_length=10, blank=True, choices=IngredientSection.choices
    )

    def __str__(self):
        return self.name

from django.contrib.postgres.fields import ArrayField
from django.db import models


class DishManager(models.Manager):
    def active(self):
        return self.filter(deactivated=False)


class Dish(models.Model):
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dishes"

    objects = DishManager()

    name = models.CharField(max_length=200, unique=True)
    recipe_url = models.URLField(max_length=300, blank=True)
    deactivated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class IngredientSection(models.TextChoices):
    """Identify different types of ingredients.

    This model lets us pull certain ingredients apart into particular sections,
    mostly based on which part of the store they're in.
    """

    MEAT = "meat", "Meat counter"
    VEG = "veg", "Fruit and veg"


class IngredientStorage(models.TextChoices):
    """Identify different storage areas for ingredients.

    This model functions very similarly to the `IngredientSection` model above, except
    that it refers to where we store ingredients once we've bought them, rather than
    where in the store we can find them. As such, it's useful during the ingredient
    sift, rather than during the shop itself.

    There's probably an argument here for combining these two models into one, but
    that's merging two separate concepts into one because they happen to be the same
    shape. Maybe if we were to add a third classification of ingredients, we could start
    looking at a more general-purpose classification model.
    """

    FREEZER = "freezer", "Freezer"
    FRIDGE = "fridge", "Fridge"
    LARDER = "larder", "Larder"


class Ingredient(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=200, unique=True)
    dishes = models.ManyToManyField(Dish, related_name="ingredients")
    section = models.CharField(
        max_length=10, blank=True, choices=IngredientSection.choices
    )
    storage = models.CharField(
        max_length=10, blank=True, choices=IngredientStorage.choices
    )

    def __str__(self):
        return self.name

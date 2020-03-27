from django.db import models


class Dish(models.Model):
    class Meta:
        verbose_name_plural = "dishes"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

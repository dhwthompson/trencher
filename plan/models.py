from django.db import models
from django.db.models.functions import Now

from dish.models import Dish


class Meal(models.Model):
    """Meal represents a planned meal.

    The meal currently has three potential states:

    - Suggested: when we're planning to eat this, but haven't got around to it yet
    - Completed: when we've eaten the meal
    - Cancelled: when we've decided not to eat the meal (or the ingredients have gone bad, or something)

    Meals can have an assigned date or not, depending on how prepared we're
    feeling.

    """

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(completed_at=None) | models.Q(cancelled_at=None),
                name="complete_cancel_exclusion",
            )
        ]

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Meal {self.id} ({self.dish.name})"

    def mark_completed(self):
        self.completed_at = Now()

    def mark_cancelled(self):
        self.cancelled_at = Now()

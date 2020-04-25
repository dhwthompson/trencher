from django.contrib import admin
from django.db.models.functions import Now

from .models import Meal


def complete_meal(modeladmin, request, queryset):
    queryset.update(completed_at=Now())


complete_meal.short_description = "Complete selected meals"


def cancel_meal(modeladmin, request, queryset):
    queryset.update(cancelled_at=Now())


cancel_meal.short_description = "Cancel selected meals"


class MealAdmin(admin.ModelAdmin):
    model = Meal

    list_display = ("__str__", "date", "created_at", "completed", "cancelled")
    actions = [complete_meal, cancel_meal]

    def completed(self, obj):
        return obj.completed_at is not None

    def cancelled(self, obj):
        return obj.cancelled_at is not None

    completed.boolean = True
    cancelled.boolean = True


admin.site.register(Meal, MealAdmin)

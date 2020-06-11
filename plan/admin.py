from django.contrib import admin
from django.db.models.functions import Now

from .models import Batch, Meal


class BatchMealAdmin(admin.TabularInline):

    model = Meal
    fields = ["dish", "date"]


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):

    model = Batch
    inlines = [BatchMealAdmin]


def complete_meal(modeladmin, request, queryset):
    queryset.update(completed_at=Now())


complete_meal.short_description = "Complete selected meals"


def cancel_meal(modeladmin, request, queryset):
    queryset.update(cancelled_at=Now())


cancel_meal.short_description = "Cancel selected meals"


class MealStateFilter(admin.SimpleListFilter):
    title = "meal state"
    parameter_name = "meal_state"

    def lookups(self, request, model_admin):
        return (
            ("suggested", "Suggested"),
            ("planned", "Planned"),
            ("eaten", "Eaten"),
            ("cancelled", "Cancelled"),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return

        filters = {
            "suggested": Meal.objects.suggested,
            "planned": Meal.objects.planned,
            "eaten": Meal.objects.eaten,
            "cancelled": Meal.objects.cancelled,
        }
        return filters[self.value()](queryset=queryset)


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    model = Meal

    list_display = ("__str__", "date", "created_at")
    list_filter = (MealStateFilter,)
    actions = [complete_meal, cancel_meal]

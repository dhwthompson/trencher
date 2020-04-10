from django.contrib import admin

from .models import Dish


class DishAdmin(admin.ModelAdmin):
    model = Dish
    ingredient_limit = 4

    list_display = ("name", "abbreviated_ingredients")

    def abbreviated_ingredients(self, obj):
        if not obj.ingredients:
            return ""
        limit = self.ingredient_limit
        if len(obj.ingredients) <= limit:
            return ", ".join(obj.ingredients)
        return (
            ", ".join(obj.ingredients[:limit])
            + f"\u2026 ({len(obj.ingredients)-limit} more)"
        )

    abbreviated_ingredients.short_description = "ingredients"


admin.site.register(Dish, DishAdmin)

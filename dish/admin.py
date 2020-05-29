from django.contrib import admin

from .models import Dish, Ingredient


class DishIngredientsAdmin(admin.TabularInline):

    model = Ingredient.dishes.through


class DishAdmin(admin.ModelAdmin):
    model = Dish
    ingredient_limit = 4

    list_display = ("name", "abbreviated_ingredients", "has_url")
    inlines = [DishIngredientsAdmin]

    def abbreviated_ingredients(self, obj):
        ingredient_count = obj.ingredients.count()

        if ingredient_count == 0:
            return ""
        limit = self.ingredient_limit
        if ingredient_count <= limit:
            return ", ".join(i.name for i in obj.ingredients.all())
        return (
            ", ".join(i.name for i in obj.ingredients.all()[:limit])
            + f"\u2026 ({ingredient_count-limit} more)"
        )

    abbreviated_ingredients.short_description = "ingredients"

    def has_url(self, obj):
        return bool(obj.recipe_url)

    has_url.boolean = True


class IngredientAdmin(admin.ModelAdmin):

    model = Ingredient

    exclude = ('dishes',)


admin.site.register(Dish, DishAdmin)
admin.site.register(Ingredient, IngredientAdmin)

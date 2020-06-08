from django.contrib import admin

from .models import Dish, Ingredient, IngredientSection


class DishIngredientsAdmin(admin.TabularInline):

    model = Ingredient.dishes.through


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    model = Dish
    ingredient_limit = 4

    list_display = ("name", "abbreviated_ingredients", "active", "has_url")
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

    def active(self, obj):
        return not obj.deactivated

    active.boolean = True

    def has_url(self, obj):
        return bool(obj.recipe_url)

    has_url.boolean = True


def assign_to_section_action(section):
    def action(modeladmin, request, queryset):
        queryset.update(section=section)

    # We need to assign each action a unique name, or Django assumes they're
    # the same action
    action.__name__ = f"assign_to_{section.value}"
    action.short_description = (
        f'Assign selected ingredients to "{section.label}" section'
    )

    return action


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    model = Ingredient

    exclude = ("dishes",)
    list_display = ("name", "section")

    actions = [assign_to_section_action(s) for s in IngredientSection]

import beeline
import itertools

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import DateField, Select, ModelForm, ModelChoiceField
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods

import waffle

from dish.models import Dish, Ingredient
from .forms import IngredientOrderForm, MealDateForm
from .models import Batch, Meal
from .groceries import GroceryList, Item
from .tracing import render


@require_GET
@login_required
def index(request):
    context = {
        "meals": Meal.objects.planned().order_by("date"),
        "page": {"title": "Now"},
    }
    return render(request, "plan/index.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def dates(request):
    meals = Meal.objects.planned().order_by("date")

    if request.method == "POST":
        items = [
            {"meal": meal, "form": MealDateForm(request.POST, instance=meal)}
            for meal in meals
        ]
        if all(item["form"].is_valid() for item in items):
            for item in items:
                item["form"].save()
            return redirect("index")
    else:
        items = [{"meal": meal, "form": MealDateForm(instance=meal)} for meal in meals]
    context = {
        "items": items,
        "page": {"title": "Now"},
    }
    return render(request, "plan/dates.html", context)


class NewMealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ["dish"]

    dish = ModelChoiceField(queryset=Dish.objects.active())


@require_http_methods(["GET", "POST"])
@login_required
def shop(request):
    if request.method == "POST":
        new_meal_form = NewMealForm(request.POST)
        try:
            new_meal_form.save()
            return redirect("shop")
        except ValueError:
            pass
    else:
        new_meal_form = NewMealForm()

    meals = Meal.objects.suggested()

    ingredient_objects = Ingredient.objects.filter(dishes__meal__in=meals)

    ingredients_form = (
        IngredientOrderForm(ingredients=ingredient_objects)
        if ingredient_objects
        else None
    )

    if waffle.flag_is_active(request, "ingredient-storage"):
        forms_by_storage = {}
        ingredients = ingredient_objects.order_by("-storage")
        for storage, storage_ingredients in itertools.groupby(
            ingredients, lambda i: i.get_storage_display()
        ):
            forms_by_storage[storage] = IngredientOrderForm(
                ingredients=storage_ingredients
            )

    no_ingredient_dishes = []
    for dish in Dish.objects.filter(meal__in=meals):
        if not dish.ingredients.count():
            no_ingredient_dishes.append(dish)

    context = {
        "meals": meals,
        "ingredients_form": ingredients_form,
        "no_ingredient_dishes": no_ingredient_dishes,
        "new_meal_form": new_meal_form,
        "page": {"title": "Next"},
    }
    if waffle.flag_is_active(request, "ingredient-storage"):
        context["forms_by_storage"] = forms_by_storage
    return render(request, "plan/shop.html", context)


@require_POST
@login_required
@transaction.atomic
def order(request):
    meals = Meal.objects.suggested()
    ingredients_form = IngredientOrderForm(
        request.POST, ingredients=Ingredient.objects.filter(dishes__meal__in=meals)
    )

    # This is super hacky, but the only validation here is that all the
    # ingredients have a value against them, and the widgets add that
    # validation client-side.
    assert ingredients_form.is_valid()

    batch = Batch.objects.create(
        ingredients_needed=[i.name for i in ingredients_form.needed]
    )
    batch.meals.set(meals)

    with beeline.tracer(name="grocery_init"):
        grocery_list = GroceryList.from_settings()

    with beeline.tracer(name="grocery_update"):
        ingredient_items = [
            Item(name=i.name, section=i.get_section_display())
            for i in ingredients_form.needed
        ]
        added = grocery_list.add_all(ingredient_items)
        already_listed = [i.name for i in ingredient_items if i not in added]
        beeline.add_context(
            {
                "ingredients.added": [i.name for i in added],
                "ingredients.already_got": ingredients_form.got,
                "ingredients.already_listed": already_listed,
            }
        )

    context = {
        "added": [i.name for i in added],
        "already_got": ingredients_form.got,
        "already_listed": already_listed,
        "page": {"title": "Order created"},
    }
    return render(request, "plan/order.html", context)


@require_POST
@login_required
def complete(request, pk):
    meal = Meal.objects.get(id=pk)
    meal.mark_completed()
    meal.save()
    return redirect("index")


@require_POST
@login_required
def cancel(request, pk):
    meal = Meal.objects.get(id=pk)
    meal.mark_cancelled()
    meal.save()
    return redirect("index")


@require_POST
@login_required
def delete(request, pk):
    meal = Meal.objects.get(id=pk)
    if meal.batch is not None:
        raise ValueError("Cannot delete a planned meal")
    meal.delete()
    return redirect("shop")

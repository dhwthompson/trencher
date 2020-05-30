import beeline

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import ModelForm
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Batch, Meal
from dish.models import Dish, Ingredient
from .groceries import GroceryList, Item
from .tracing import render


@require_GET
@login_required
def index(request):
    context = {"meals": Meal.objects.planned().order_by("date")}
    return render(request, "plan/index.html", context)


class NewMealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ["dish"]


@require_http_methods(["GET", "POST"])
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

    dishes = Dish.objects.filter(meal__in=meals)
    no_ingredient_dishes = []

    ingredients = Ingredient.objects.filter(dishes__meal__in=meals).values_list(
        "name", flat=True
    )

    for dish in dishes:
        if not dish.ingredients.count():
            no_ingredient_dishes.append(dish)

    context = {
        "meals": meals,
        "ingredients": ingredients,
        "no_ingredient_dishes": no_ingredient_dishes,
        "new_meal_form": new_meal_form,
    }
    return render(request, "plan/shop.html", context)


@require_POST
@login_required
@transaction.atomic
def order(request):
    ingredient_objects = Ingredient.objects.filter(name__in=request.POST)
    ingredients_by_name = {i.name: i for i in ingredient_objects}
    ingredients_got = [
        ingredients_by_name[i] for i, status in request.POST.items() if status == "have"
    ]
    ingredients_needed = [
        ingredients_by_name[i] for i, status in request.POST.items() if status == "need"
    ]
    batch = Batch.objects.create(
        ingredients_needed=[i.name for i in ingredients_needed]
    )
    batch.meals.set(Meal.objects.suggested())

    with beeline.tracer(name="grocery_init"):
        grocery_list = GroceryList.from_settings()

    with beeline.tracer(name="grocery_update"):
        ingredient_items = [
            Item(name=i.name, section=i.get_section_display())
            for i in ingredients_needed
        ]
        added = grocery_list.add_all(ingredient_items)
        already_listed = [i.name for i in ingredient_items if i not in added]
        beeline.add_context(
            {
                "ingredients.added": [i.name for i in added],
                "ingredients.already_got": ingredients_got,
                "ingredients.already_listed": already_listed,
            }
        )

    context = {
        "added": [i.name for i in added],
        "already_got": ingredients_got,
        "already_listed": already_listed,
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

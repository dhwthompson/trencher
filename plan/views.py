from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import ModelForm
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Batch, Meal
from .groceries import GroceryList
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
    ingredients = set()
    no_ingredient_dishes = []
    for meal in meals:
        ingredients = ingredients.union(meal.dish.ingredients)
        if not meal.dish.ingredients:
            no_ingredient_dishes.append(meal.dish)

    context = {
        "meals": meals,
        "ingredients": sorted(ingredients),
        "no_ingredient_dishes": no_ingredient_dishes,
        "new_meal_form": new_meal_form,
    }
    return render(request, "plan/shop.html", context)


@require_POST
@login_required
@transaction.atomic
def order(request):
    ingredients_got = [
        ingredient for ingredient, status in request.POST.items() if status == "have"
    ]
    ingredients_needed = [
        ingredient for ingredient, status in request.POST.items() if status == "need"
    ]
    batch = Batch.objects.create(ingredients_needed=ingredients_needed)
    batch.meals.set(Meal.objects.suggested())

    grocery_list = GroceryList.from_settings()
    added = grocery_list.add_all(batch.ingredients_needed)
    already_listed = [i for i in ingredients_needed if i not in added]

    context = {
        "added": added,
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

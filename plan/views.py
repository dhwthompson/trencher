from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Meal


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
    for meal in meals:
        ingredients = ingredients.union(meal.dish.ingredients)

    context = {"meals": Meal.objects.suggested(), "ingredients": ingredients, "new_meal_form": new_meal_form}
    return render(request, "plan/shop.html", context)


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

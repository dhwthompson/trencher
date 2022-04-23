from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import NewDishForm
from .models import Dish, Ingredient


@require_http_methods(["GET", "POST"])
@login_required
@transaction.atomic
def new(request):
    if request.method == "GET":
        context = {"form": NewDishForm()}
        return render(request, "dish/new.html", context)
    else:
        form = NewDishForm(request.POST)
        if not form.is_valid():
            return render(request, "dish/new.html", {"form": form})

        new_dish = Dish(name=form.cleaned_data["name"])
        ingredient_names = [
            name.strip() for name in form.cleaned_data["ingredients"].splitlines()
        ]
        ingredients = [
            Ingredient.objects.get_or_create(name=n)[0] for n in ingredient_names
        ]
        new_dish.save()
        new_dish.ingredients.add(*ingredients)

        return redirect("index")

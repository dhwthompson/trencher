from django.shortcuts import render

from .models import Dish


def index(request):
    context = {"dishes": Dish.objects.order_by("name")}
    return render(request, "dish/index.html", context)

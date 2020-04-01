from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Dish


@login_required
def index(request):
    context = {"dishes": Dish.objects.order_by("name")}
    return render(request, "dish/index.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import Meal


@require_GET
@login_required
def index(request):
    meals = Meal.objects.filter(completed_at=None, cancelled_at=None).order_by("date")

    context = {"meals": meals}
    return render(request, "plan/index.html", context)


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

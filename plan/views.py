from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Meal


@require_GET
@login_required
def index(request):
    meals = Meal.objects.filter(completed_at=None, cancelled_at=None).order_by("date")

    context = {"meals": meals}
    return render(request, "plan/index.html", context)

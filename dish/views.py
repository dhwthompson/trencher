from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import Dish


class NewDishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self["name"].field.widget.attrs["required"] = "required"


@require_http_methods(['GET', 'POST'])
@login_required
def index(request):
    if request.method == "POST":
        form = NewDishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewDishForm()

    context = {"dishes": Dish.objects.order_by("name"), "form": form}
    return render(request, "dish/index.html", context)

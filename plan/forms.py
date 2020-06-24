from datetime import timedelta

from django import forms
from django.utils import timezone

from .dates import date_name
from .models import Meal


INGREDIENT_CHOICES = (
    ("have", "Got it"),
    ("need", "Need it"),
)


class InvalidFormError(Exception):
    """Error for attempting to access properties on an invalid form."""

    pass


class IngredientOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        ingredients = kwargs.pop("ingredients")
        super(IngredientOrderForm, self).__init__(*args, **kwargs)
        for ingredient in ingredients:
            self.fields[ingredient.name] = forms.ChoiceField(
                choices=INGREDIENT_CHOICES, widget=forms.RadioSelect()
            )

        self._ingredients_by_name = {i.name: i for i in ingredients}

    @property
    def needed(self):
        if not self.is_valid():
            raise InvalidFormError("Ingredients form is not valid")
        return [
            self._ingredients_by_name[i]
            for i, status in self.cleaned_data.items()
            if status == "need"
        ]

    @property
    def got(self):
        if not self.is_valid():
            raise InvalidFormError("Ingredients form is not valid")
        return [
            self._ingredients_by_name[i]
            for i, status in self.cleaned_data.items()
            if status == "have"
        ]


def week_choices(today, include=None):
    """Return available scheduling choices for the next week.

    Include a "None" option, to remove an already-scheduled date.

    The `include` argument will make sure that a specified date is in the list
    of choices, for forms where a date outside the usual range is already
    scheduled.
    """
    unset_choice = ("", "-- Unscheduled --")
    days = {today + timedelta(days=offset) for offset in range(7)}
    if include is not None:
        days.add(include)

    return [unset_choice] + [
        (day.isoformat(), date_name(day, today=today)) for day in sorted(days)
    ]


class MealDateForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["date"]

    def __init__(self, *args, **kwargs):
        today_func = kwargs.pop("today_func", timezone.localdate)
        instance = kwargs["instance"]
        prefix = str(instance.id)
        super(MealDateForm, self).__init__(*args, **kwargs, prefix=prefix)

        # We need to set this up explicitly on init so that the the date
        # choices are calculated each time, rather than baked in at load time.
        date_widget = forms.Select(
            choices=week_choices(today=today_func(), include=instance.date)
        )
        date_field = forms.DateField(required=False, widget=date_widget)
        date_field.label = ""
        self.fields["date"] = date_field

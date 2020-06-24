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


def choice_for_date(date, today=None):
    return (date.isoformat(), date_name(date, today))


def week_choices():
    """Return available scheduling choices for the next week.

    Include a "None" option, to remove an already-scheduled date.
    """
    today = timezone.localdate()
    choices = [("", "-- Unscheduled --")]
    for offset in range(7):
        date = today + timedelta(days=offset)
        choices.append(choice_for_date(date))
    return choices


class MealDateForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["date"]

    def __init__(self, *args, **kwargs):
        prefix = str(kwargs["instance"].id)
        super(MealDateForm, self).__init__(*args, **kwargs, prefix=prefix)
        if not self._instance_date_in_choices():
            date_widget = self.fields["date"].widget
            date_widget.choices = sorted(
                date_widget.choices + [choice_for_date(self.instance.date)]
            )

    def _instance_date_in_choices(self):
        if self.instance is None or self.instance.date is None:
            return True

        choice_values = [c[0] for c in self.fields["date"].widget.choices]
        return self.instance.date.isoformat() in choice_values

    date = forms.DateField(required=False, widget=forms.Select(choices=week_choices()))
    date.label = ""

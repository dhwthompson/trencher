from django import forms


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

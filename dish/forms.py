from django import forms

class NewDishForm(forms.Form):
    name = forms.CharField(label="Dish name", max_length=200)
    ingredients = forms.CharField(label="Ingredients", widget=forms.Textarea)

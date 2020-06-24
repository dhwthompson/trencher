from datetime import date

from django.test import TestCase

from dish.models import Ingredient
from .forms import IngredientOrderForm, MealDateForm
from .models import Meal


class IngredientOrderFormTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.bulk_create(
            [Ingredient(name=i) for i in ["Ham", "Egg", "Chips"]]
        )

    def test_field_names(self):
        ingredients = Ingredient.objects.all()
        form = IngredientOrderForm(ingredients=ingredients)

        self.assertEqual([i.name for i in ingredients], [field.name for field in form])

    def test_empty_post(self):
        ingredients = Ingredient.objects.all()
        post_data = {}

        form = IngredientOrderForm(ingredients=ingredients)

        self.assertFalse(form.is_valid())

    def test_partial_post(self):
        ingredients = Ingredient.objects.all()
        post_data = {ingredients[0].name: "need", ingredients[1].name: "have"}

        form = IngredientOrderForm(ingredients=ingredients)

        self.assertFalse(form.is_valid())

    def test_need_everything(self):
        ingredients = Ingredient.objects.all()
        post_data = {ingredient.name: "need" for ingredient in ingredients}

        form = IngredientOrderForm(post_data, ingredients=ingredients)

        self.assertTrue(form.is_valid())
        self.assertEqual(len(ingredients), len(form.needed))
        self.assertEqual(0, len(form.got))

    def test_got_everything(self):
        ingredients = Ingredient.objects.all()
        post_data = {ingredient.name: "have" for ingredient in ingredients}

        form = IngredientOrderForm(post_data, ingredients=ingredients)

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.needed))
        self.assertEqual(len(ingredients), len(form.got))


class MealDateFormTestCase(TestCase):
    def test_unset_option_exists(self):
        meal = Meal()
        form = MealDateForm(instance=meal)

        date_choices = form.fields["date"].widget.choices
        self.assertEqual(date_choices[0], ("", "-- Unscheduled --"))

    def test_no_date_set(self):
        meal = Meal()
        today_func = lambda: date(2020, 2, 2)
        form = MealDateForm(instance=meal, today_func=today_func)

        self.assertEqual(
            form.fields["date"].widget.choices,
            [
                ("", "-- Unscheduled --"),
                ("2020-02-02", "Today"),
                ("2020-02-03", "Tomorrow"),
                ("2020-02-04", "Tuesday"),
                ("2020-02-05", "Wednesday"),
                ("2020-02-06", "Thursday"),
                ("2020-02-07", "Friday"),
                ("2020-02-08", "Saturday"),
            ],
        )

    def test_date_in_range(self):
        today_func = lambda: date(2020, 2, 2)
        meal = Meal(date(2020, 2, 4))
        form = MealDateForm(instance=meal, today_func=today_func)

        self.assertEqual(
            form.fields["date"].widget.choices,
            [
                ("", "-- Unscheduled --"),
                ("2020-02-02", "Today"),
                ("2020-02-03", "Tomorrow"),
                ("2020-02-04", "Tuesday"),
                ("2020-02-05", "Wednesday"),
                ("2020-02-06", "Thursday"),
                ("2020-02-07", "Friday"),
                ("2020-02-08", "Saturday"),
            ],
        )

    def test_date_out_of_range(self):
        today_func = lambda: date(2020, 2, 2)
        meal = Meal(date=date(2020, 2, 1))
        form = MealDateForm(instance=meal, today_func=today_func)

        self.assertEqual(
            form.fields["date"].widget.choices,
            [
                ("", "-- Unscheduled --"),
                ("2020-02-01", "Saturday 1 Feb"),
                ("2020-02-02", "Today"),
                ("2020-02-03", "Tomorrow"),
                ("2020-02-04", "Tuesday"),
                ("2020-02-05", "Wednesday"),
                ("2020-02-06", "Thursday"),
                ("2020-02-07", "Friday"),
                ("2020-02-08", "Saturday"),
            ],
        )

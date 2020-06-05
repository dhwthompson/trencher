from django.test import TestCase

from dish.models import Ingredient

from .forms import IngredientOrderForm


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

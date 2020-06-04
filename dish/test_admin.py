from django.test import TestCase
from .admin import DishAdmin
from .models import Dish, Ingredient


class DishAdminTestCase(TestCase):
    def setUp(self):
        self.admin = DishAdmin(Dish, admin_site=None)

    def test_no_ingredients(self):
        dish = Dish.objects.create(name="Tasty food")
        self.assertEqual(self.admin.abbreviated_ingredients(dish), "")

    def test_short_ingredient_list(self):
        dish = Dish.objects.create(name="Tasty food")
        for ingredient in ["Ham", "Eggs"]:
            dish.ingredients.create(name=ingredient)
        self.assertEqual(self.admin.abbreviated_ingredients(dish), "Eggs, Ham")

    def test_ingredient_list_at_limit(self):
        dish = Dish.objects.create(name="Tasty food")
        for ingredient in ["Ham", "Eggs", "Chips", "Beans"]:
            dish.ingredients.create(name=ingredient)
        self.assertEqual(self.admin.abbreviated_ingredients(dish), "Beans, Chips, Eggs, Ham")

    def test_ingredient_list_over_limit(self):
        dish = Dish.objects.create(name="Tasty food")
        for ingredient in ["Ham", "Eggs", "Chips", "Beans", "Sausage", "Caviar"]:
            dish.ingredients.create(name=ingredient)
        self.assertEqual(
            self.admin.abbreviated_ingredients(dish),
            "Beans, Caviar, Chips, Eggs\u2026 (2 more)",
        )

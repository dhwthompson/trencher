from django.test import TestCase
from .admin import DishAdmin
from .models import Dish


class DishAdminTestCase(TestCase):
    def setUp(self):
        self.admin = DishAdmin(Dish, admin_site=None)

    def test_no_ingredients(self):
        dish = Dish(ingredients=[])
        self.assertEqual(self.admin.abbreviated_ingredients(dish), "")

    def test_short_ingredient_list(self):
        dish = Dish(ingredients=["Ham", "Eggs"])
        self.assertEqual(self.admin.abbreviated_ingredients(dish), "Ham, Eggs")

    def test_ingredient_list_at_limit(self):
        dish = Dish(ingredients=["Ham", "Eggs", "Chips", "Beans"])
        self.assertEqual(self.admin.abbreviated_ingredients(dish), "Ham, Eggs, Chips, Beans")

    def test_ingredient_list_over_limit(self):
        dish = Dish(ingredients=["Ham", "Eggs", "Chips", "Beans", "Sausage", "Caviar"])
        self.assertEqual(
            self.admin.abbreviated_ingredients(dish),
            "Ham, Eggs, Chips, Beans\u2026 (2 more)",
        )

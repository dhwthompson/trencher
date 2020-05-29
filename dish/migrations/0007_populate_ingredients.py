# Generated by Django 3.0.4 on 2020-05-29 00:20

from django.db import migrations


def populate_ingredient_model(apps, schema_editor):
    Dish = apps.get_model('dish', 'Dish')
    Ingredient = apps.get_model('dish', 'Ingredient')

    for dish in Dish.objects.all():
        for ingredient_name in dish.ingredients:
            i, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            i.dishes.add(dish)


def populate_ingredient_field(apps, schema_editor):
    Dish = apps.get_model('dish', 'Dish')
    Ingredient = apps.get_model('dish', 'Ingredient')

    for dish in Dish.objects.all():
        dish_ingredients = Ingredient.objects.filter(dishes=dish)
        dish.ingredients = [i.name for i in dish_ingredients]
        dish.save()


class Migration(migrations.Migration):

    dependencies = [
        ("dish", "0006_ingredient"),
    ]

    operations = [
        migrations.RunPython(populate_ingredient_model, populate_ingredient_field)
    ]

from django.contrib import admin

from .models import Dish


class DishAdmin(admin.ModelAdmin):
    model = Dish


admin.site.register(Dish, DishAdmin)

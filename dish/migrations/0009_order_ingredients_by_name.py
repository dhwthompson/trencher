# Generated by Django 3.0.4 on 2020-05-29 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0008_remove_ingredients_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name']},
        ),
    ]

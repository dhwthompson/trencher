# Generated by Django 3.0.4 on 2020-04-10 21:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0002_dishes_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, size=None),
        ),
    ]
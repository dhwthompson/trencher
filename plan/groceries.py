import todoist

from django.conf import settings as django_settings


class GroceryList(object):
    def __init__(self, access_token, project_id):
        self._api = todoist.api.TodoistAPI(access_token)
        self._api.sync()
        self._project_id = project_id

    @classmethod
    def from_settings(cls, settings=django_settings):
        return cls(settings.TODOIST_ACCESS_TOKEN, settings.TODOIST_PROJECT_ID)

    def _has_item(self, item):
        items = [
            i["content"]
            for i in self._api.items.all()
            if i["project_id"] == self._project_id
        ]
        return item in items

    def add_all(self, ingredients):
        added_ingredients = []
        for ingredient in ingredients:
            if not self._has_item(ingredient):
                self._api.items.add(content=ingredient, project_id=self._project_id)
                added_ingredients.append(ingredient)
        self._api.commit()
        return added_ingredients

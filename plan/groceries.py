import todoist

from django.conf import settings as django_settings

from dataclasses import dataclass


@dataclass
class Item:
    name: str
    section: str = None


class GroceryList(object):
    def __init__(self, access_token, project_id):
        self._api = todoist.api.TodoistAPI(access_token)
        self._api.sync()
        self._project_id = project_id

    @classmethod
    def from_settings(cls, settings=django_settings):
        return cls(settings.TODOIST_ACCESS_TOKEN, settings.TODOIST_PROJECT_ID)

    def _items(self):
        # Make sure we only return items that haven't been completed
        return self._api.items.all(
            lambda i: i["project_id"] == self._project_id and not i["checked"]
        )

    def _section_id(self, section_name):
        """Return the ID of the section with the given name.

        If the section does not exist, return None.
        """
        sections = self._api.sections.all(
            lambda s: s["project_id"] == self._project_id
            and not (s["is_archived"] or s["is_deleted"])
        )

        for section in sections:
            if section["name"] == section_name:
                return section["id"]

    def _has_item(self, item):
        for i in self._items():
            if i["content"] == item.name:
                return True

        return False

    def add_all(self, ingredients):
        added_ingredients = []
        for ingredient in ingredients:
            section_id = (
                self._section_id(ingredient.section) if ingredient.section else None
            )

            if not self._has_item(ingredient):
                self._api.items.add(
                    content=ingredient.name,
                    project_id=self._project_id,
                    section_id=section_id,
                    checked=False,
                )
                added_ingredients.append(ingredient)
        self._api.commit()
        return added_ingredients

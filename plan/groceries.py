import todoist

from django.conf import settings as django_settings


class Item:
    """An item to add to the grocery list.

    This class isn't much more than a two-value record, with a name and a
    section. The section is None by default.
    """

    def __init__(self, name, section=None):
        self.name = name
        self.section = section

    def __repr__(self):
        if self.section is not None:
            return f'Item({self.name!r}, section={self.section!r})'
        else:
            return f'Item({self.name!r})'


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

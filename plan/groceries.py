import beeline
import json
import todoist

from django.conf import settings as django_settings
from django.core.cache import cache


class CachingTodoistAPI(todoist.api.TodoistAPI):

    """A subclassed version of the Todoist API that supports flexible caching.

    The official version of the Todoist API only supports caching to a
    directory in the file system, but it'd be nice to be able to use the
    Django cache instead, as we don't have file system access.

    The `cache` keyword argument should be something following the Django cache
    API <https://docs.djangoproject.com/en/3.0/topics/cache/#basic-usage>.
    Namely, it should have the methods:

        get(key)
        cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None)
    """

    STATE_KEY = "todoist_state"
    SYNC_TOKEN_KEY = "todoist_sync_token"

    def __init__(self, *args, **kwargs):
        cache_obj = kwargs.get("cache")
        if hasattr(cache_obj, "get") and hasattr(cache_obj, "set"):
            kwargs.pop("cache")
            self.cache_obj = cache_obj
        else:
            # Defer to the superclass implementation of a directory cache
            self.cache_obj = None

        super(CachingTodoistAPI, self).__init__(*args, **kwargs)

    @beeline.traced(name="todoist_cache_read")
    def _read_cache(self):
        if self.cache_obj is None:
            super(CachingTodoistAPI, self)._read_cache()
            return

        state = self.cache_obj.get(self.STATE_KEY)
        beeline.add_context(
            {
                "state_cache_hit": state is not None,
                "state_cache_length": len(state or ""),
            }
        )

        if state:
            self._update_state(json.loads(state))

        sync_token = self.cache_obj.get(self.SYNC_TOKEN_KEY)
        beeline.add_context({"sync_token_cache_hit": sync_token is not None})
        self.sync_token = sync_token

    @beeline.traced(name="todoist_cache_write")
    def _write_cache(self):
        if self.cache_obj is None:
            super(CachingTodoistAPI, self)._write_cache()
            return

        result = json.dumps(
            self.state, indent=2, sort_keys=True, default=todoist.api.state_default
        )

        beeline.add_context({"state_cache_length": len(result or "")})

        self.cache_obj.set(self.STATE_KEY, result, timeout=None)
        self.cache_obj.set(self.SYNC_TOKEN_KEY, self.sync_token, timeout=None)


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
            return f"Item({self.name!r}, section={self.section!r})"
        else:
            return f"Item({self.name!r})"


class GroceryList(object):
    def __init__(self, access_token, project_id):
        self._api = CachingTodoistAPI(access_token, cache=cache)
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

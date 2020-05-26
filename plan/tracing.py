import beeline

from django.shortcuts import render as django_render


def render(request, template_name, *args, **kwargs):
    """Render a Django response with some extra instrumentation.

    This is designed to be a drop-in replacement for Django's standard `render`
    shortcut, but such that it will automatically provide tracing information
    (to track down any slow-rendering templates) and add some extra context.
    """
    beeline.add_context({"template_name": template_name})
    with beeline.tracer(name="template_render"):
        return django_render(request, template_name, *args, **kwargs)

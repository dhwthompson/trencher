import beeline

from waffle.models import Flag


class BeelineFlagMiddleware(object):
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        beeline.add_context(
            {f"flag.{flag.name}": flag.is_active(request) for flag in Flag.get_all()}
        )
        return self._get_response(request)

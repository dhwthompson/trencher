import beeline


class BeelineAuthMiddleware(object):
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        beeline.add_context(
            {
                "user.authenticated": request.user.is_authenticated,
                "user.id": request.user.id,
            }
        )
        return self._get_response(request)

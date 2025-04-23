import json

from django.http import JsonResponse


def Success(payload):
    return JsonResponse(dict(code=200, payload=payload), safe=False, status=200)


class JsonRequest:
    def __init__(self, request):
        self._request = request

    def _json(self) -> dict:
        if self._request.content_type == 'application/json':
            return json.loads(self._request.body)
        return None

    def body(self):
        return self._json()

    def get(self, key, default=None):
        _result = self._json()
        if _result is not None: return _result.get(key, default)

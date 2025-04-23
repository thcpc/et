from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from label import service
from libs.http_handle import JsonRequest


# Create your views here.

@require_GET
def get_labels(request):
    return JsonResponse(dict(code=200, payload=service.get_labels()))


@require_POST
@csrf_exempt
def new_label(request):
    # category, name
    json_request = JsonRequest(request)
    category = json_request.get('categoryId')
    name = json_request.get('name')
    resp = service.new_label(category, name)
    return JsonResponse(dict(code=200, payload=resp))
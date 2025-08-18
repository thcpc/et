from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from et_document.label import service as label_service
from libs.http_handle import JsonRequest


@require_GET
def get_labels(request):
    return JsonResponse(dict(code=200, payload=label_service.get_labels()))


@require_POST
# @csrf_exempt
def new_label(request):
    # category, name
    json_request = JsonRequest(request)
    category = json_request.get('categoryId')
    name = json_request.get('name')
    resp = label_service.new_label(category, name)
    return JsonResponse(dict(code=200, payload=resp))
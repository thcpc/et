from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from libs.http_handle import JsonRequest, Success
from libs.utils import get_header_token, decode_jwt
from user import service


# Create your views here.


@require_POST
@csrf_exempt
def login(request):
    r = JsonRequest(request)
    user_name = r.get("username")
    password = r.get("password")
    finger_print = r.get('fingerPrint')
    if user_name:
        auth_token = service.login_by_name(user_name, password, finger_print)
    else:
        old_token = get_header_token(request)
        auth_token = service.login_by_finger(old_token, finger_print, password)
    return Success(payload=auth_token)


@require_GET
def device(request):
    _finger_print = request.GET.get("fingerPrint")
    pay_load = service.device(_finger_print)
    return Success(payload=pay_load)


@require_POST
@csrf_exempt
def register(request):
    r = JsonRequest(request)
    user_name = r.get("username")
    password = r.get("password")
    resp_body = service.register(user_name, password)
    return Success(payload=resp_body)


@require_GET
def users(request):
    token = get_header_token(request)
    self_user_id = decode_jwt(token, verify=False)["user_id"]
    pay_load = service.users(self_user_id)
    return Success(payload=pay_load)

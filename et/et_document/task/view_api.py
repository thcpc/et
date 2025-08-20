from django.views.decorators.http import require_GET, require_POST

from libs.http_handle import JsonRequest, Success
from libs.jwt_utils import get_header_token, decode_jwt
from et_document.task import service as task_service

@require_GET
def get_tasks(request):
    token = get_header_token(request)
    page_no = int(request.GET.get("pageNo"))
    per_count = int(request.GET.get("perCount"))
    user_id = decode_jwt(token, verify=False)["user_id"]
    payload = task_service.get_tasks(user_id, page_no, per_count)
    return Success(payload=payload)


@require_POST
# @csrf_exempt
def re_assign(request):
    req_data = JsonRequest(request)
    _task_id = req_data.get("task_id")
    _new_assignee = req_data.get('new_assignee_id')
    _old_assignee = req_data.get('old_assignee_id')
    _comment = req_data.get("comment")

    payload = task_service.re_assign(task_id=_task_id,
                                new_assignee_user_id=_new_assignee,
                                old_assignee_id=_old_assignee,
                                comment=_comment)
    return Success(payload=payload)


@require_POST
# @csrf_exempt
def roll_back(request):
    req_data = JsonRequest(request)
    _task_id = int(req_data.get("task_id"))
    _comment = req_data.get("comment")
    task_service.roll_back(_task_id, _comment)
    return Success(payload={})
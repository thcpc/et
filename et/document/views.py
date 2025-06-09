import os
from datetime import datetime
from time import perf_counter_ns

import jwt
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_GET, require_POST

from document import service
from et import enums
from taskdispatcher import service as task_center
# from et import settings
from libs.http_handle import JsonRequest
from libs.mocks import Mock
from libs.utils import get_header_token, decode_jwt
from taskdispatcher.core.task_definition.task_define import TaskDefine
from taskdispatcher.core.task_definition.taskgenerator import TaskGenerator


# Create your views here.


@require_GET
def page(request):
    """
    http://...../?pageId={int}
    """
    _page_id = request.GET.get("pageId")
    # paragraphs = Mock.get_paragraphs(page_id)
    _paragraphs = service.get_paragraphs(_page_id)

    return JsonResponse(dict(code=200, payload=_paragraphs), safe=False)


@require_GET
def all_document(request):
    page_no = int(request.GET.get("pageNo"))
    per_count = int(request.GET.get("perCount"))
    _documents = service.get_all_documents(page_no=page_no, per_count=per_count)
    return JsonResponse(dict(code=200, payload=_documents), safe=False)


@require_GET
def user_documents(request):
    page_no = int(request.GET.get("pageNo"))
    per_count = int(request.GET.get("perCount"))
    token = get_header_token(request)
    user_name = decode_jwt(token).get("username")
    _documents = service.get_user_documents(user_name=user_name, page_no=page_no, per_count=per_count)
    return JsonResponse(dict(code=200, payload=_documents), safe=False)


@require_POST
@csrf_exempt
def new_document(request):
    json_request = JsonRequest(request)
    name = json_request.get('name')
    labels = json_request.get('labels')
    token = get_header_token(request)
    author = decode_jwt(token).get("username")
    _document = service.new_document(author, name, labels)
    return JsonResponse(dict(code=200, payload=_document), safe=False)


@require_POST
@csrf_exempt
def update_document(request):
    _update_document = JsonRequest(request).get("document")
    service.update_document(_update_document)
    return JsonResponse(dict(code=200, payload={}), safe=False)


@require_GET
def pages(request):
    doc_id = request.GET.get("docId")
    _pages = Mock.get_pages(doc_id)
    return JsonResponse(dict(code=200, payload=_pages), safe=False)


@require_GET
def document(request):
    """
    http://...../?docId={int}
    """
    _doc_id = int(request.GET.get("docId"))
    _include_page = True if request.GET.get("includePage") == 'true' else False
    _data = service.get_document(_doc_id, _include_page)
    # _pages = Mock.get_pages(doc_id)
    return JsonResponse(dict(code=200, payload=dict(document=_data[0],
                                                    pages=_data[1]
                                                    )), safe=False)


# @require_POST
# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
#
#         # 生成唯一的文件名
#         file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + uploaded_file.name
#
#         # 保存文件到 media 目录
#         save_path = os.path.join(settings.MEDIA_ROOT, file_name)
#         with open(save_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
#
#         # 返回文件的 URL
#         file_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
#         return JsonResponse(dict(code=200, payload=dict(url=file_url), safe=False))


@require_POST
@csrf_exempt
def new_paragraph(request):
    _contents = JsonRequest(request).get('contents', '')
    _page_id = int(JsonRequest(request).get('pageId'))
    _paragraph_type = JsonRequest(request).get('paragraphType')
    data = service.new_paragraph(_page_id, _contents, _paragraph_type)

    return JsonResponse(
        dict(code=200, payload=data, safe=False))


@require_POST
@csrf_exempt
def new_snapshot(request):
    json_request = JsonRequest(request)
    _doc_id = json_request.get("docId")
    _name = json_request.get("name")
    _description = json_request.get("description")
    service.snapshot(_doc_id, _name, _description)
    _user_id = decode_jwt(get_header_token(request), verify=False)["user_id"]
    # task_center.dispatcher.delay(
    #     AssignAutoTask.spec(document_id=_doc_id, create_user_id=_user_id, assign_user_id=_user_id,
    #                         current_task_id=None))
    task_center.dispatcher(
        TaskGenerator.definition(TaskDefine(document_id=_doc_id,
                                            create_user_id=None,
                                            old_assign_user_id=None,
                                            new_assign_user_id=_user_id,
                                            current_task_id=None,
                                            comment=None,
                                            task_type=enums.Name.TaskType.AssignAutoTaskGenerator)))
    # task_center.dispatcher.delay(RegressionTask.spec(document_id=_doc_id, user_id=_user_id))
    # task_center.dispatcher(AutoTask.spec(document_id=_doc_id, user_id=_user_id))
    # task_center.dispatcher(RegressionTask.spec(document_id=_doc_id, user_id=_user_id))
    return JsonResponse(dict(code=200, payload={}), safe=False)


@require_POST
@csrf_exempt
def update_paragraph(request):
    contents = JsonRequest(request).get('contents', '')
    paragraph_id = JsonRequest(request).get('paragraphId')
    # Mock.update_paragraph(paragraph_id=paragraph_id, contents=contents)
    service.update_paragraph(paragraph_id=paragraph_id, contents=contents)
    return JsonResponse(dict(code=200, payload=dict(), safe=False))


@require_POST
@csrf_exempt
def move_paragraph(request):
    change_orders = JsonRequest(request).get('changeOrders')
    # Mock.move_paragraph(change_orders)
    service.move_paragraph(change_orders)
    return JsonResponse(dict(code=200, payload=dict(), safe=False))


@csrf_exempt
def delete_paragraph(request):
    if request.method == "DELETE":
        paragraph_id = request.GET.get("paragraphId")
        # Mock.delete_paragraph(paragraph_id=paragraph_id)
        service.delete_paragraph(paragraph_id=paragraph_id)
        return JsonResponse(dict(code=200, payload=dict(), safe=False))
    else:
        return HttpResponseNotAllowed(['DELETE'])


@csrf_exempt
def delete_document(request):
    if request.method == "DELETE":
        _document_id = request.GET.get("documentId")
        # Mock.delete_paragraph(paragraph_id=paragraph_id)
        service.delete_document(document_id=_document_id)
        return JsonResponse(dict(code=200, payload=dict(), safe=False))
    else:
        return HttpResponseNotAllowed(['DELETE'])

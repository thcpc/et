from django.urls import path


from . import views

urlpatterns = [
    path("api/get/page", view=views.doc_view_api.page, name="page"),
    path("api/documents", view=views.doc_view_api.all_document, name="documents"),
    path("api/user/documents", view=views.doc_view_api.user_documents, name="user_documents"),

    path("api/document", view=views.doc_view_api.document, name="document"),
    path("api/new/document", view=views.doc_view_api.new_document, name="new_document"),
    path("api/delete/document", view=views.doc_view_api.delete_document, name="delete_document"),
    path("api/update/document", view=views.doc_view_api.update_document, name="update_document"),
    path("api/document/page", view=views.doc_view_api.document, name="document"),
    # path("api/upload-image", view=views.upload_image, name="upload_image"),
    path("api/new/paragraph", view=views.doc_view_api.new_paragraph, name="new_paragraph"),
    path("api/update/paragraph", view=views.doc_view_api.update_paragraph, name="update_paragraph"),
    path("api/move/paragraph", view=views.doc_view_api.move_paragraph, name="move_paragraph"),
    path("api/delete/paragraph", view=views.doc_view_api.delete_paragraph, name="delete_paragraph"),
    path("api/new/snapshot", view=views.doc_view_api.new_snapshot, name="new_paragraph"),
    path("api/labels", view=views.label_view_api.get_labels, name="get_labels"),
    path("api/new/label", view=views.label_view_api.new_label, name="new_label"),

    path("api/user/tasks", view=views.task_view_api.get_tasks, name="tasks"),
    path("api/reAssignee", view=views.task_view_api.re_assign, name='re_assignee'),
    path("api/rollBack", view=views.task_view_api.roll_back, name='roll_back')

]

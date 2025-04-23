from django.urls import path


from . import views

urlpatterns = [
    path("api/page", view=views.page, name="page"),
    path("api/documents", view=views.all_document, name="documents"),
    path("api/user/documents", view=views.user_documents, name="user_documents"),

    path("api/document", view=views.document, name="document"),
    path("api/new/document", view=views.new_document, name="new_document"),
    path("api/delete/document", view=views.delete_document, name="delete_document"),
    path("api/update/document", view=views.update_document, name="update_document"),
    path("api/page", view=views.document, name="document"),
    # path("api/upload-image", view=views.upload_image, name="upload_image"),
    path("api/new/paragraph", view=views.new_paragraph, name="new_paragraph"),
    path("api/update/paragraph", view=views.update_paragraph, name="update_paragraph"),
    path("api/move/paragraph", view=views.move_paragraph, name="move_paragraph"),
    path("api/delete/paragraph", view=views.delete_paragraph, name="delete_paragraph"),
    path("api/new/snapshot", view=views.new_snapshot, name="new_paragraph")

]

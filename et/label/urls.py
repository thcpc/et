from django.urls import path


from . import views

urlpatterns = [
    path("api/labels", view=views.get_labels, name="get_labels"),
    path("api/new/label", view=views.new_label, name="new_label")
]

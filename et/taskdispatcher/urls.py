from django.urls import path


from . import views

urlpatterns = [
    path("api/user/tasks", view=views.get_tasks, name="tasks"),
    path("api/reAssignee", view=views.re_assign, name='re_assignee'),
    path("api/rollBack", view=views.roll_back, name='roll_back')


]

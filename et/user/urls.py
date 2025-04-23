from django.urls import path


from . import views

urlpatterns = [
    path("api/login", view=views.login, name="login"),
    path("api/register", view=views.register, name="register"),
    path("api/device", view=views.device, name="device"),
    path("api/users", view=views.users, name="users")

]

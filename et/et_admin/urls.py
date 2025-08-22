from django.urls import path


from . import views

urlpatterns = [
    path("api/login", view=views.user_view_api.login, name="login"),
    path("api/register", view=views.user_view_api.register, name="register"),
    path("api/device", view=views.user_view_api.device, name="device"),
    path("api/users", view=views.user_view_api.users, name="users"),
    path("api/logout", view=views.user_view_api.logout, name="logout")

]

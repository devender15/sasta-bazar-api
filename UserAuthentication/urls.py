from django.urls import path
from .views import RegisterUser, ListUsers, LoginView, UserProfileView


urlpatterns = [
    path('show-users', ListUsers.as_view()),
    path('register', RegisterUser.as_view()),
    path('login', LoginView.as_view()),
    path('get-user', UserProfileView.as_view()),
]

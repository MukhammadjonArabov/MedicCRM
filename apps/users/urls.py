from django.urls import path, include
from apps.users.views import (
    LoginView,
    LogoutView,
    RefreshView,
    UserView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', RefreshView.as_view(), name='auth_register'),
    path('user/', UserView.as_view(), name='auth_user'),
]
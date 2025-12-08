from django.urls import path, include
from drf_yasg.utils import swagger_auto_schema
from apps.users.views import (
    LoginView, LogoutView, RefreshView, UserView, UserRegisterView
)

# user_register = swagger_auto_schema(tags=["Users"])(UserRegisterView.as_view())

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', RefreshView.as_view(), name='auth_register'),
    path('user/', UserView.as_view(), name='auth_user'),
    path('register/', UserRegisterView.as_view(), name='auth_register'),
]
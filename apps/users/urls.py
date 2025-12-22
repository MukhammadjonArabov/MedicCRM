from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    LoginView,
    LogoutView,
    RefreshView,
    UserView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # -------- AUTH --------
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', RefreshView.as_view(), name='auth_refresh'),

    # -------- CURRENT USER --------
    path('me/', UserView.as_view(), name='auth_user'),
    path('', include(router.urls)),
]

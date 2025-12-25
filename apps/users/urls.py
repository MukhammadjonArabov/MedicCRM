from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    LoginView,
    LogoutView,
    RefreshView,
    UserView,
    UserViewSet,
    DoctorListView,
    StaffScheduleListView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # -------- AUTH --------
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', RefreshView.as_view(), name='auth_refresh'),
    path('me/', UserView.as_view(), name='auth_me'),

    # -------- USERS --------
    path('staff-schedules/', StaffScheduleListView.as_view(), name='staff-schedule-list'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('', include(router.urls)),
]

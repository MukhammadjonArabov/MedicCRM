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
    StaffScheduleCreateView,
    StaffScheduleUpdateView,
    PatientViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'patients', PatientViewSet, basename='patient')

urlpatterns = [
    # -------- AUTH --------
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/refresh/', RefreshView.as_view(), name='auth_refresh'),
    path('auth/me/', UserView.as_view(), name='auth_me'),

    # -------- USERS --------
    path('staff-schedules/', StaffScheduleListView.as_view(), name='staff_schedule_list'),
    path('staff-schedules/create/', StaffScheduleCreateView.as_view(), name='staff_schedule_create'),
    path('staff-schedules/<int:pk>/update/', StaffScheduleUpdateView.as_view(), name='staff_schedule_update'),
    path('users/doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('', include(router.urls)),
]

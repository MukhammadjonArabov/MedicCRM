from rest_framework import generics, status
from rest_framework.response import Response
from apps.meeting.models import Meeting, Queue
from django.utils.timezone import localdate
from apps.users.views import BaseAPIView
from apps.meeting.serializers import (
    MeetingCreateSerializer,
    MeetingDoctorListSerializer,
    MeetingListSerializer,
    MeetingRetrieveSerializer,
    MeetingDoctorRetrieveSerializer,
    MeetingUpdateSerializer,
    MeetingStatusUpdateSerializer,
    MeetingDailySerializer
)
from apps.users.permissions import IsAdminOrRegistrar, IsDoctorOrAdminOrRegistrar


class MeetingCreateAPIView(generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingCreateSerializer
    permission_classes = [IsAdminOrRegistrar]


class MeetingListAPIView(BaseAPIView, generics.ListAPIView):
    permission_classes = [IsDoctorOrAdminOrRegistrar]

    def get_queryset(self):
        if self.is_swagger():
            return Meeting.objects.none()

        user = self.get_user()
        role = self.get_user_role()

        qs = Meeting.objects.select_related('doctor', 'patient')

        if role in ['admin', 'registrar']:
            return qs

        if role == 'doctor':
            return qs.filter(doctor=user)

        return qs.none()

    def get_serializer_class(self):
        return (
            MeetingDoctorListSerializer
            if self.get_user_role() == 'doctor'
            else MeetingListSerializer
        )


class MeetingRetriveAPIView(BaseAPIView, generics.RetrieveAPIView):
    permission_classes = [IsDoctorOrAdminOrRegistrar]
    lookup_field = 'pk'

    def get_queryset(self):

        if self.is_swagger():
            return Meeting.objects.none()

        user = self.get_user()
        role = self.get_user_role()

        if not user:
            return Meeting.objects.none()

        queryset = Meeting.objects.select_related('doctor', 'patient')

        if role in ['admin', 'registrar']:
            return queryset.order_by('-date_time')

        if role == 'doctor':
            return queryset.filter(doctor=user).order_by('-date_time')

        return Meeting.objects.none()

    def get_serializer_class(self):
        if self.is_swagger():
            return MeetingRetrieveSerializer

        return (
            MeetingDoctorRetrieveSerializer
            if self.get_user_role() == 'doctor'
            else MeetingRetrieveSerializer
        )

class MeetingUpdateAPIView(generics.UpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingUpdateSerializer
    permission_classes = [IsAdminOrRegistrar]
    http_method_names = ['patch']


class MeetingStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingStatusUpdateSerializer
    permission_classes = [IsDoctorOrAdminOrRegistrar]
    http_method_names = ['patch']


class DailyMeetingListAPIView(BaseAPIView, generics.ListAPIView):
    serializer_class = MeetingDailySerializer
    permission_classes = [IsDoctorOrAdminOrRegistrar]

    def get_queryset(self):
        if self.is_swagger():
            return Meeting.objects.none()

        user = self.get_user()
        role = self.get_user_role()

        if not user.is_authenticated:
            return Meeting.objects.none()

        today = localdate()
        queryset = Meeting.objects.filter(date_time__date=today)

        if role in ['admin', 'registrar']:
            return queryset

        elif role == 'doctor':
            return queryset.filter(doctor=user)

        return Meeting.objects.none()

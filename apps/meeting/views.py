from rest_framework import generics
from rest_framework.exceptions import ValidationError
from apps.meeting.models import Meeting
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
    MeetingDailySerializer,
    MeetingListDoctorSerializer
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


class MeetingRetrieveAPIView(BaseAPIView, generics.RetrieveAPIView):
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


class MonthMeetingListAPIView(BaseAPIView, generics.ListAPIView):
    serializer_class = MeetingDailySerializer
    permission_classes = [IsAdminOrRegistrar]

    def get_queryset(self):
        if self.is_swagger():
            return Meeting.objects.none()

        params = self.request.query_params
        year = params.get('year')
        month = params.get('month')

        if not year or not month:
            raise ValidationError({"detail": "year and month are required"})

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            raise ValidationError({"detail": "year and month must be integers"})

        return (
            Meeting.objects
            .filter(date_time__year=year, date_time__month=month)
            .select_related('doctor', 'patient')
            .order_by('-date_time')
        )


class DoctorMeetingListView(generics.RetrieveAPIView):
    serializer_class = MeetingListDoctorSerializer
    queryset = Meeting.objects.all()
    permission_classes = [IsAdminOrRegistrar]




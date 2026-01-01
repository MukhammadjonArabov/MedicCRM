from rest_framework import generics, status
from rest_framework.response import Response
from apps.meeting.models import Meeting, Queue
from apps.meeting.serializers import (
    MeetingCreateSerializer, MeetingListSerializer, MettingDoctorListSerializer
    )
from apps.users.permissions import IsAdminOrRegistrar, IsDoctorOrAdminOrRegistrar

class MeetingCreateAPIView(generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingCreateSerializer
    permission_classes = [IsAdminOrRegistrar]

class MeetingListAPIView(generics.ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingListSerializer
    permission_classes = [IsDoctorOrAdminOrRegistrar]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'registrar']:
            return Meeting.objects.all().order_by('-date_time')
        
        elif user.role == 'doctor':
            return Meeting.objects.filter(doctor=user).order_by('-date_time')
        
        return Meeting.objects.none()
    
    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if user.role == 'doctor':
            kwargs['context'] = self.get_serializer_context()
            return MettingDoctorListSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

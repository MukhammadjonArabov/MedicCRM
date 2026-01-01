from rest_framework import generics, status
from rest_framework.response import Response
from apps.meeting.models import Meeting, Queue
from apps.meeting.serializers import (
        MeetingCreateSerializer, MeetingDoctorListSerializer, MeetingListSerializer, MeetingRetrieveSerializer,
        MeetingDoctorRetrieveSerializer, MeetingUpdateSerializer
    )
from apps.users.permissions import IsAdminOrRegistrar, IsDoctorOrAdminOrRegistrar


class MeetingCreateAPIView(generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingCreateSerializer
    permission_classes = [IsAdminOrRegistrar]


class MeetingListAPIView(generics.ListAPIView):
    permission_classes = [IsDoctorOrAdminOrRegistrar]

    def get_queryset(self):
        user = self.request.user

        doctor_or_patient = Meeting.objects.select_related('doctor', 'patient')

        if user.role in ['admin', 'registrar']:
            return doctor_or_patient.order_by('-date_time')
        
        elif user.role == 'doctor':
            return doctor_or_patient.filter(doctor=user).order_by('-date_time')
        
        return Meeting.objects.none() 
    
    def get_serializer_class(self):
       user = self.request.user

       return (
           MeetingDoctorListSerializer if user.role == 'doctor' else MeetingListSerializer
       )
    

class MeetingRetriveAPIView(generics.RetrieveAPIView):
    parmission_classes = [IsDoctorOrAdminOrRegistrar]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user

        doctor_or_patient = Meeting.objects.select_related('doctor', 'patient')

        if user.role in ['admin', 'registrar']:
            return doctor_or_patient.order_by('-date_time')
        
        elif user.role == 'doctor':
            return doctor_or_patient.filter(doctor=user).order_by('-date_time')
        
        return Meeting.objects.none()
    
    def get_serializer_class(self):
        user = self.request.user

        return (
            MeetingDoctorRetrieveSerializer if user.role == 'doctor' else MeetingRetrieveSerializer
        )
    

class MeetingUpdateAPIView(generics.UpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingUpdateSerializer
    permission_classes = [IsAdminOrRegistrar]
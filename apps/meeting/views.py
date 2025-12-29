from rest_framework import generics, status
from rest_framework.response import Response
from apps.meeting.models import Meeting, Queue
from apps.meeting.serializers import MeetingCreateSerializer
from apps.users.permissions import IsAdminOrRegistrar

class MeetingCreateAPIView(generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingCreateSerializer
    permission_classes = [IsAdminOrRegistrar]

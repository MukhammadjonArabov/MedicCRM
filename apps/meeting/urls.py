from django.urls import path, include

from apps.meeting.views import MeetingCreateAPIView
urlpatterns = [
    path('meeting-create/', MeetingCreateAPIView.as_view(), name='meeting_create'),
]
from django.urls import path, include

from apps.meeting.views import MeetingCreateAPIView, MeetingListAPIView
urlpatterns = [
    path('meeting-create/', MeetingCreateAPIView.as_view(), name='meeting_create'),
    path('meeting_list/', MeetingListAPIView.as_view(), name='meeting_list'),
]


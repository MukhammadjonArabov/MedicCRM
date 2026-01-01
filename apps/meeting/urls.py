from django.urls import path, include

from apps.meeting.views import MeetingCreateAPIView, MeetingListAPIView, MeetingRetriveAPIView
urlpatterns = [
    path('meeting-create/', MeetingCreateAPIView.as_view(), name='meeting_create'),
    path('meeting_list/', MeetingListAPIView.as_view(), name='meeting_list'),
    path('meeting_retrieve/<int:pk>/', MeetingRetriveAPIView.as_view(), name='meeting_retrieve'),

]
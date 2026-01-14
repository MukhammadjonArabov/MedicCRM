from django.urls import path, include

from apps.meeting.views import( 
    MeetingCreateAPIView, MeetingListAPIView, MeetingRetrieveAPIView, MeetingUpdateAPIView,
    MeetingStatusUpdateAPIView, DailyMeetingListAPIView, MonthMeetingListAPIView, DoctorMeetingListView
    )


urlpatterns = [
    path('meeting-create/', MeetingCreateAPIView.as_view(), name='meeting_create'),
    path('meeting_list/', MeetingListAPIView.as_view(), name='meeting_list'),
    path('meeting_retrieve/<int:pk>/', MeetingRetrieveAPIView.as_view(), name='meeting_retrieve'),
    path('meeting-update/<int:pk>/', MeetingUpdateAPIView.as_view(), name='meeting_update'),
    path('meetings/<int:pk>/status/', MeetingStatusUpdateAPIView.as_view(), name='meeting_update_status'),
    path('meetings/daily/', DailyMeetingListAPIView.as_view(), name='daily_meeting'),
    path('meetings/monthly/', MonthMeetingListAPIView.as_view(), name='monthly_meeting'),
    path('meeting/doctor/<int:pk>/', DoctorMeetingListView.as_view(), name='doctor_meeting'),
]
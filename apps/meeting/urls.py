from django.urls import path, include

from apps.meeting.views import( 
    MeetingCreateAPIView, MeetingListAPIView, MeetingRetriveAPIView, MeetingUpdateAPIView,
    MeetingStatusUpdateAPIView
    )
urlpatterns = [
    path('meeting-create/', MeetingCreateAPIView.as_view(), name='meeting_create'),
    path('meeting_list/', MeetingListAPIView.as_view(), name='meeting_list'),
    path('meeting_retrieve/<int:pk>/', MeetingRetriveAPIView.as_view(), name='meeting_retrieve'),
    path('meeting-update/<int:pk>/', MeetingUpdateAPIView.as_view(), name='meeting_update'),
    path('meetings/<int:pk>/status/', MeetingStatusUpdateAPIView.as_view(), name='meeting_update_status'),

]
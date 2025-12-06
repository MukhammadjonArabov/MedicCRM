from django.contrib import admin
from apps.meeting.models import Meeting, Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('doctor__full_name', 'patient__full_name', 'status')
    list_filter = ('status',)

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('doctor__full_name', 'patient__full_name', 'date_time', 'status', 'created_by')
    list_filter = ('status', 'created_by')
    search_fields = ('doctor__full_name', 'patient__full_name')


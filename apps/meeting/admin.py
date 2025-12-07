from django.contrib import admin
from apps.meeting.models import Meeting, Queue

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor_name', 'patient_name', 'status')
    list_filter = ('status',)
    search_fields = ('doctor__full_name', 'patient__full_name')

    def doctor_name(self, obj):
        return obj.doctor.full_name
    doctor_name.short_description = "Doctor"

    def patient_name(self, obj):
        return obj.patient.full_name
    patient_name.short_description = "Patient"

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor_name', 'patient_name', 'date_time', 'status', 'created_by')
    list_filter = ('status', 'created_by')
    search_fields = ('doctor__full_name', 'patient__full_name')

    def doctor_name(self, obj):
        return obj.doctor.full_name
    doctor_name.short_description = "Doctor"

    def patient_name(self, obj):
        return obj.patient.full_name
    patient_name.short_description = "Patient"



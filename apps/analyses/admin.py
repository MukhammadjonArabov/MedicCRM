from django.contrib import admin
from django.utils.html import format_html
from .models import Analyses, Prescriptions, AuditLog, MedicalRecords


@admin.register(Analyses)
class AnalysesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "analysis_type",
        "status",
        "created_at",
        "file_preview",
    )
    list_filter = ("status", "created_at")
    search_fields = ("patient__full_name", "analysis_type")

    autocomplete_fields = ("patient",)

    def file_preview(self, obj):
        if obj.file:
            return format_html(
                "<a href='{}' target='_blank'>📄 File</a>",
                obj.file.url
            )
        return "—"
    file_preview.short_description = "File"


@admin.register(Prescriptions)
class PrescriptionsAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "created_at")
    search_fields = (
        "patient__full_name",
        "doctor__full_name",
    )
    list_filter = ("doctor", "created_at")

    autocomplete_fields = ("patient", "doctor")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "entity", "entity_id", "created_at")
    search_fields = ("user__full_name", "action", "entity")
    list_filter = ("entity", "created_at")

    readonly_fields = ("user", "action", "entity", "entity_id", "created_at")

    ordering = ("-created_at",)


@admin.register(MedicalRecords)
class MedicalRecordsAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "created_at")
    search_fields = (
        "patient__full_name",
        "doctor__full_name",
        "diagnosis",
        "treatment",
    )
    list_filter = ("doctor", "created_at")

    autocomplete_fields = ("patient", "doctor")

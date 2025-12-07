from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Patients


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def image_tag(self, obj):
        if obj.image_user:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:15px;" />'.format(obj.image_user.url))
        return "-"
    image_tag.short_description = "Image"

    list_display = ("image_tag", "full_name", "email", "phone_number", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("full_name", "email", "phone_number")  
    ordering = ("email",)

    fieldsets = (
        ("Login Info", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone_number", "image_user", "descriptor")}),
        ("Role & Permissions", {"fields": ("role", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone_number", "image_user", "role", "password1", "password2"),
        }),
    )

@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image_patient:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:15px;" />'.format(obj.image_patient.url))
        return "-"
    image_tag.short_description = "Image"

    list_display = ("image_tag", "full_name", "phone_number", "gender", "birth_date")
    search_fields = ("full_name", "phone_number")
    list_filter = ("gender",)
    ordering = ("full_name",)

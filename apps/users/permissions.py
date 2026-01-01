from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.role == 'doctor'
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role == 'admin'
        )


class IsDoctorOrAdminOrRegisterOrNurse(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.role in ['doctor', 'nurse', 'admin', 'registrar']
        )


class IsDoctorOrAdminOrRegistrar(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.role in ['doctor', 'admin', 'registrar']
        )


class IsAdminOrRegistrar(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.role in ['admin', 'registrar']
        )


class IsDoctorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.role in ['doctor', 'admin']
        )


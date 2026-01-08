from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class BaseRolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        user = request.user
        if not user or isinstance(user, AnonymousUser):
            return False
        return getattr(user, 'role', None) in self.allowed_roles


class IsDoctor(BaseRolePermission):
    allowed_roles = ['doctor']


class IsAdmin(BaseRolePermission):
    allowed_roles = ['admin']


class IsDoctorOrAdminOrRegisterOrNurse(BaseRolePermission):
    allowed_roles = ['doctor', 'nurse', 'admin', 'registrar']


class IsDoctorOrAdminOrRegistrar(BaseRolePermission):
    allowed_roles = ['doctor', 'admin', 'registrar']


class IsAdminOrRegistrar(BaseRolePermission):
    allowed_roles = ['admin', 'registrar']


class IsDoctorOrAdmin(BaseRolePermission):
    allowed_roles = ['doctor', 'admin']

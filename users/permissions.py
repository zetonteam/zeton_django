from users.models import Role, Caregiver
from rest_framework import permissions


class IsUserCaregiver(permissions.BasePermission):
    def has_permission(self, request, view):
        return Caregiver.objects.filter(user_id=request.user.id).exists()


class HasUserAccessToStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return Role.objects.filter(
            student_id=view.kwargs.get("student_id"), caregiver__user_id=request.user.id
        ).exists()

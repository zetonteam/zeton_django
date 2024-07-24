from users.models import Role
from rest_framework import permissions


class HasUserAccessToStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return Role.objects.filter(
            student_id=view.kwargs.get("student_id"), caregiver__user_id=request.user.id
        ).exists()


def has_caregiver_access_to_student(caregiver_id, student_id) -> bool:
    # TODO:
    # This permission is currently not used anywhere-
    # we could probably remove it.

    res = Role.objects.filter(student_id=student_id, caregiver_id=caregiver_id).exists()

    return res

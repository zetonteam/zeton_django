from users.models import Role


def has_user_access_to_student(user_id, student_id) -> bool:
    res = Role.objects.filter(
        student_id=student_id, caregiver__user_id=user_id
    ).exists()

    return res


def has_caregiver_access_to_student(caregiver_id, student_id) -> bool:
    res = Role.objects.filter(student_id=student_id, caregiver_id=caregiver_id).exists()

    return res

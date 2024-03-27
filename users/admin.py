from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Caregiver, CustomUser, Role, Student


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_auth",
    ]
    empty_value_display = "unknown"


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    model = Caregiver
    inlines = (RoleInline,)
    list_display = ["user", "first_name", "last_name", "email"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = (RoleInline,)
    list_display = ["user", "first_name", "last_name", "email", "total_points"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"

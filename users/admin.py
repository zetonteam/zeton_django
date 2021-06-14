from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Caregiver, Student


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_auth', ]


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    model = Caregiver
    list_display = ['user', 'first_name', 'last_name', 'email']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'total_points']

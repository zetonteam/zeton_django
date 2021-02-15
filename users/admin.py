from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Caregiver


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['first_name', 'last_name', 'email', 'is_auth', ]


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    list_display = ['user']

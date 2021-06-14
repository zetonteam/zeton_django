from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Caregiver, Student


# @admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_auth', ]
    # inlines = [CaregiverAdminInline, ]


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    model = Caregiver
    list_display = ['user']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points']


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Caregiver)

# test comment

from django.urls import path

from users.resources import StudentsResource, students_resource

urlpatterns = [
    path("students/<int:pk>", StudentsResource.as_view(), name="student-resource"),
    path("students", StudentsResource.as_view(), name="students-resource"),

    # path("students/<int:pk>", students_resource, name="student-resource"),
    # path("students", students_resource, name="students-resource"),
]

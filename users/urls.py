from django.urls import path

from users.resources import StudentsResource, PrizesResource

urlpatterns = [
    path("students/<int:pk>", StudentsResource.as_view(), name="student-resource"),
    path("students", StudentsResource.as_view(), name="students-resource"),

    path("prizes/<int:pk>", PrizesResource.as_view(), name="student-resource"),
    path("prizes", PrizesResource.as_view(), name="students-resource"),
]

from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from users.views import (
    current_user,
    StudentsResource,
    PrizesResource,
    SinglePrizeResource,
    TasksResource,
    SingleTaskResource,
    PointResource,
)

urlpatterns = [
    path("token-auth/", token_obtain_pair),
    path("current-user/", current_user),
    path("students/", StudentsResource.as_view(), name="students-resource"),
    path(
        "students/<int:student_id>/",
        StudentsResource.as_view(),
        name="student-resource",
    ),
    path(
        "students/<int:student_id>/points/",
        PointResource.as_view(),
        name="points-resource",
    ),
    path(
        "students/<int:student_id>/prizes/",
        PrizesResource.as_view(),
        name="prizes-resource",
    ),
    path(
        "students/<int:student_id>/prize/<int:prize_id>",
        SinglePrizeResource.as_view(),
        name="prize-resource",
    ),
    path(
        "students/<int:student_id>/tasks/",
        TasksResource.as_view(),
        name="tasks-resource",
    ),
    path(
        "students/<int:student_id>/task/<int:task_id>",
        SingleTaskResource.as_view(),
        name="task-resource",
    ),
]

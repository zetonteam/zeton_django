from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from users.views import (
    UserList,
    current_user,
    StudentsResource,
    PrizesResource,
    TasksResource,
    PointResource,
    ClaimPrizeResource,
)

urlpatterns = [
    path("token-auth/", obtain_jwt_token),
    path("current-user/", current_user),
    path("register/", UserList.as_view()),
    path("students/", StudentsResource.as_view(), name="students-resource"),
    path("students/<int:pk>/", StudentsResource.as_view(), name="student-resource"),
    path("students/<int:pk>/points/", PointResource.as_view(), name="points-resource"),
    path("students/<int:pk>/prizes/", PrizesResource.as_view(), name="prizes-resource"),
    path(
        "students/<int:pk_student>/prizes/<int:pk_prize>/claim",
        ClaimPrizeResource.as_view(),
        name="claim-prize-resource",
    ),
    path("students/<int:pk>/tasks/", TasksResource.as_view(), name="tasks-resource"),
]

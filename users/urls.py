from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from users.resources import (
    PointResource,
    PrizesResource,
    StudentsResource,
    TasksResource,
)
from users.views import UserList, current_user

urlpatterns = [
    path("token-auth/", obtain_jwt_token),
    path("current-user/", current_user),
    path("register/", UserList.as_view()),
    path("students/", StudentsResource.as_view(), name="students-resource"),
    path("students/<int:pk>/", StudentsResource.as_view(), name="student-resource"),
    path("students/<int:pk>/points/", PointResource.as_view(), name="points-resource"),
    path("students/<int:pk>/prizes/", PrizesResource.as_view(), name="prizes-resource"),
    path("tasks/", TasksResource.as_view(), name="tasks-resource"),
    path("tasks/<int:pk>/", TasksResource.as_view(), name="task-resource"),
]

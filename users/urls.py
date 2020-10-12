from django.urls import path

from users.resources import StudentsResource, PrizesResource, TasksResource

urlpatterns = [
    path("students/<int:pk>/", StudentsResource.as_view(), name="student-resource"),
    path("students/", StudentsResource.as_view(), name="students-resource"),

    path("prizes/<int:pk>/", PrizesResource.as_view(), name="prize-resource"),
    path("prizes/", PrizesResource.as_view(), name="prizes-resource"),

    path("tasks/<int:pk>/", TasksResource.as_view(), name="task-resource"),
    path("tasks/", TasksResource.as_view(), name="tasks-resource"),
]

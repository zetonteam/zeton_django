from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from users.resources import StudentsResource, CaregiversResource, PrizesResource, TasksResource, PointResource

from users.views import current_user, UserList

urlpatterns = [
    path('token-auth/', obtain_jwt_token),

    path('current-user/', current_user),
    path('register/', UserList.as_view()),

    path("students/<int:pk>/", StudentsResource.as_view(), name="student-resource"),
    path("students/", StudentsResource.as_view(), name="students-resource"),

    path("caregivers/<int:pk>/", CaregiversResource.as_view(), name="caregiver-resource"),

    path("prizes/<int:pk>/", PrizesResource.as_view(), name="prize-resource"),
    path("prizes/", PrizesResource.as_view(), name="prizes-resource"),

    path("tasks/<int:pk>/", TasksResource.as_view(), name="task-resource"),
    path("tasks/", TasksResource.as_view(), name="tasks-resource"),

    path("points/", PointResource.as_view(), name="points-resource"),
    path("points/<int:pk>/", PointResource.as_view(), name="point-resource")
]

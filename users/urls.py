from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from users import views
from users.resources import StudentsResource, PrizesResource, TasksResource

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('hello/', views.HelloView.as_view(), name='hello'),

    path("students/<int:pk>/", StudentsResource.as_view(), name="student-resource"),
    path("students/", StudentsResource.as_view(), name="students-resource"),

    path("prizes/<int:pk>/", PrizesResource.as_view(), name="prize-resource"),
    path("prizes/", PrizesResource.as_view(), name="prizes-resource"),

    path("tasks/<int:pk>/", TasksResource.as_view(), name="task-resource"),
    path("tasks/", TasksResource.as_view(), name="tasks-resource"),
]

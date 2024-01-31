
from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from users.resources import StudentsResource, CaregiversResource, PrizesResource, TasksResource, PointResource

from users.views import current_user, UserList

urlpatterns = [
    path("/", PointResource.as_view(), name="points-resource"),

]
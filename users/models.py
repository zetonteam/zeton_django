from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_auth = models.BooleanField(null=True, blank=True)

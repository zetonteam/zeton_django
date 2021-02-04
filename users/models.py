from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_auth = models.BooleanField(null=True, blank=True)


class Caregiver(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_points = models.IntegerField()


class Point(models.Model):
    value = models.IntegerField()
    assigner = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    assignee = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_date = models.DateTimeField(auto_now_add=True)


class Prize(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField()


class Task(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField()
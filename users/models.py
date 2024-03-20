from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CustomUser(AbstractUser):
    is_auth = models.BooleanField(null=True, blank=True)


class Caregiver(models.Model):
    """ 
    Caregiver contains data about account holders and relational users (Students).
    One user can be connected to many Caregivers (one-many).
    It may contain more than one Students (many-many).

    TODO:
    - ID for each Caregiver.
    - LifeRole (eg. Parent, Teacher, Therapist) for each Caregiver.
    - SuperSuperCaregiver
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "caregivers"

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def first_name(self):
        return self.user.first_name

    first_name.short_description = "First Name"

    def last_name(self):
        return self.user.last_name

    last_name.short_description = "Last Name"

    def email(self):
        return self.user.email

    email.short_description = "email"


class Student(models.Model):
    class Meta:
        db_table = "students"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_points = models.IntegerField()
    caregivers = models.ManyToManyField(Caregiver, related_name='students', through='Role')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def first_name(self):
        return self.user.first_name

    first_name.short_description = "First Name"

    def last_name(self):
        return self.user.last_name

    last_name.short_description = "Last Name"

    def email(self):
        return self.user.email

    email.short_description = "email"


class Role(models.Model):
    class Meta:
        db_table = "roles"

    class RoleNameChoice(models.TextChoices):
        CAREGIVER = 'caregiver'

    role_name = models.CharField(max_length=30, choices=RoleNameChoice.choices)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role_name} | {self.caregiver.user.first_name}"


class Point(models.Model):
    class Meta:
        db_table = "student_points"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    TASK_TYPE = "task"
    PRIZE_TYPE = "prize"

    POINTS_TYPE = (
        (TASK_TYPE, "task"),
        (PRIZE_TYPE,  "prize"),
    )

    value = models.IntegerField()

    assigner = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_date = models.DateTimeField(auto_now_add=True)
    points_type = models.CharField(max_length=20, choices=POINTS_TYPE, default=PRIZE_TYPE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Prize(models.Model):
    class Meta:
        db_table = "student_prizes"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField()


class Task(models.Model):
    class Meta:
        db_table = "student_tasks"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField()

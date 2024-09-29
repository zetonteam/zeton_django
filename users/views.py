from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Caregiver, Student, Prize, Task, Point
from .permissions import HasUserAccessToStudent

from .serializers import (
    CustomUserSerializer,
    CustomUserSerializerWithToken,
    StudentSerializer,
    PrizeSerializer,
    TaskSerializer,
    PointSerializer,
    PointShortSerializer,
    RoleSerializer,
)


@api_view(["GET"])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CustomUserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentsResource(APIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        try:
            caregiver = Caregiver.objects.get(user_id=user_id)
        except Caregiver.DoesNotExist:
            raise PermissionDenied()

        students = caregiver.students.all()
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)

    def post(self, request):
        try:
            user_id = request.user.id
            caregiver_id = Caregiver.objects.get(user_id=user_id).id
        except Caregiver.DoesNotExist:
            raise PermissionDenied()

        # Create new student entry.
        student_serializer = StudentSerializer(data=request.data)
        student_serializer.is_valid(raise_exception=True)
        student_serializer.save()

        # Add a role.
        role_data = {
            "role_name": "caregiver",
            "caregiver": caregiver_id,
            "student": student_serializer.data["pk"],
        }
        role_serializer = RoleSerializer(data=role_data)
        role_serializer.is_valid(raise_exception=True)
        role_serializer.save()

        return Response(student_serializer.data)


class SingleStudentResource(APIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        serializer = StudentSerializer(student)

        return Response(serializer.data)

    def patch(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PrizesResource(APIView):
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id):
        prizes = Prize.objects.filter(student_id=student_id)
        serializer = PrizeSerializer(prizes, many=True)
        return Response(serializer.data)

    def post(self, request, student_id):
        serializer = PrizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student_id=student_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SinglePrizeResource(APIView):
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id, prize_id):
        prize = get_object_or_404(Prize, pk=prize_id, student_id=student_id)
        serializer = PrizeSerializer(prize)
        return Response(serializer.data)

    def patch(self, request, student_id, prize_id):
        prize = get_object_or_404(Prize, pk=prize_id, student_id=student_id)
        serializer = PrizeSerializer(prize, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, student_id, prize_id):
        prize = get_object_or_404(Prize, pk=prize_id, student_id=student_id)
        prize.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TasksResource(APIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id):
        tasks = Task.objects.filter(student_id=student_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, student_id):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student_id=student_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleTaskResource(APIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id, task_id):
        task = get_object_or_404(Task, pk=task_id, student_id=student_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, student_id, task_id):
        task = get_object_or_404(Task, pk=task_id, student_id=student_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, student_id, task_id):
        task = get_object_or_404(Task, pk=task_id, student_id=student_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PointResource(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]
    serializer_class = PointShortSerializer

    def get_queryset(self):
        queryset = Point.objects.filter(student_id=self.kwargs["student_id"])
        return queryset.order_by("-assignment_date")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PointShortSerializer()
        else:
            return PointSerializer

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name="page",
                description="number of page from pagination",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="page_size",
                description="number of records in page for pagination",
                required=False,
                type=int,
            ),
        ],
        # override default docstring extraction
        description="Endpoint to generate last records of points of particular student by pagination",
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def get(self, request, student_id):
        user_id = request.user.id
        try:
            _ = Caregiver.objects.get(user_id=user_id)
        except Caregiver.DoesNotExist:
            raise PermissionDenied()

        query_set = self.get_queryset()
        page = self.paginate_queryset(query_set)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        # extra parameters added to the schema
        request=PointShortSerializer,
        # parameters=[
        #     OpenApiParameter(
        #         name="content_type",
        #         description="task or prize",
        #         required=True,
        #         type=str,
        #     ),
        #     OpenApiParameter(
        #         name="object_id",
        #         description="task_id or prize_id",
        #         required=True,
        #         type=int,
        #     ),
        # ],
        # override default docstring extraction
        # description="Endpoint to generate last records of points of particular student by pagination",
        # change the auto-generated operation name
        # operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        # operation=None,
    )
    def post(self, request, student_id):
        content_type = request.data.get("content_type")
        object_id = request.data.get("object_id")
        student = Student.objects.get(pk=student_id)

        # Get points type and points difference.
        if content_type == "task":
            content_object = Task.objects.get(pk=object_id, student=student)
            total_points_diff = content_object.value
        elif content_type == "prize":
            content_object = Prize.objects.get(pk=object_id, student=student)
            total_points_diff = -content_object.value
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        caregiver = Caregiver.objects.get(user=request.user)
        content_type_obj = ContentType.objects.get(model=content_type)

        # Get new total points value.
        new_total_points = student.total_points + total_points_diff

        # Prevent going below zero.
        if new_total_points < 0:
            error_data = {"detail": "Total points cannot be negative."}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error_data)

        # Save new Point.
        serializer = PointSerializer(
            data={
                "student": student.pk,
                "assigner": caregiver.pk,
                "value": content_object.value,
                "content_object": content_object,
                "points_type": content_type,
                "content_type": content_type_obj.pk,
                "object_id": object_id,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Modify student's total points.
        student.total_points = new_total_points
        student.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

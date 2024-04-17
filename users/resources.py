from django.http.response import Http404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Caregiver, Point, Prize, Student, Task
from users.permissions import HasUserAccessToStudent
from users.serializers import (
    PointSerializer,
    PrizeSerializer,
    StudentSerializer,
    TaskSerializer,
)


class StudentsResource(APIView):
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.kwargs.get(
            "pk"
        ):  # PK is provided- user wants to extract data for a single student
            return [permissions.IsAuthenticated(), HasUserAccessToStudent()]
        else:
            return [permissions.IsAuthenticated()]

    def get(self, request, pk=None):
        user_id = request.user.id
        if pk is None:
            try:
                caregiver = Caregiver.objects.get(user_id=user_id)
            except Caregiver.DoesNotExist:
                raise PermissionDenied

            students = caregiver.students.all()
            serializer = StudentSerializer(students, many=True)
        else:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)

        return Response(serializer.data)

    # TODO future
    # def post(self, request):
    #     serializer = StudentSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    def patch(self, request, pk):
        user_id = request.user.id
        if pk is None:
            raise MethodNotAllowed

        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# TODO future
# def delete(self, request, pk):
#     Student.objects.filter(pk=pk).delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class PrizesResource(APIView):
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, pk):
        prizes = Prize.objects.filter(student_id=pk)
        serializer = PrizeSerializer(prizes, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = PrizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TasksResource(APIView):
    def get(self, request, pk=None):
        if pk is None:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
        else:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = PrizeSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        Task.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PointResource(generics.GenericAPIView):
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get_queryset(self):
        if self.kwargs.get("pk") is not None:
            resource_id = self.kwargs["pk"]
        else:
            resource_id = self.request.query_params.get("studentId", None)
            if resource_id is None:
                raise Http404

        queryset = Point.objects.all()
        queryset = queryset.filter(student_id=resource_id)
        return queryset.order_by("-assignment_date")

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
    def get(self, request, pk=None, format=None):
        user_id = request.user.id
        try:
            _ = Caregiver.objects.get(user_id=user_id)
        except Caregiver.DoesNotExist:
            raise PermissionDenied

        query_set = self.get_queryset()
        page = self.paginate_queryset(query_set)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

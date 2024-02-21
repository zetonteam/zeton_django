from django.db.models import F
from django.http.response import Http404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Student, Caregiver, Prize, Task, Point
from users.permissions import has_user_access_to_student
from users.serializers import StudentSerializer, PrizeSerializer, TaskSerializer, PointSerializer


class StudentsResource(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
            if has_user_access_to_student(user_id, pk):
                student = Student.objects.get(pk=pk)
                serializer = StudentSerializer(student)
            else:
                raise PermissionDenied

        return Response(serializer.data)


#TODO future
    # def post(self, request):
    #     serializer = StudentSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


    def patch(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
#TODO future
    # def delete(self, request, pk):
    #     Student.objects.filter(pk=pk).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class PrizesResource(APIView):
    def get(self, request, pk=None):
        if pk is None:
            prizes = Prize.objects.all()
            serializer = PrizeSerializer(prizes, many=True)
        else:
            prize = Prize.objects.get(pk=pk)
            serializer = PrizeSerializer(prize)
        return Response(serializer.data)

    def post(self, request):
        serializer = PrizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        prize = Prize.objects.get(pk=pk)
        serializer = PrizeSerializer(prize, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        prize = Prize.objects.get(pk=pk)
        serializer = PrizeSerializer(prize, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        Prize.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.kwargs.get('pk') is not None:
            resource_id = self.kwargs['pk']
        else:
            resource_id = self.request.query_params.get('studentId', None)
            if resource_id is None:
                raise Http404

        queryset = Point.objects.all()
        queryset = queryset.filter(student_id=resource_id)
        return queryset

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(name='studentId', description='Filter by studentId', required=False, type=int)
        ],
        # override default docstring extraction
        description='Endpoint to generate points of particular student',
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def get(self, request, pk=None, format=None):
        point = self.get_queryset()
        if pk is not None:
            serializer = PointSerializer(point.first())
        else:
            serializer = PointSerializer(point, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            points = serializer.save()
            points.student.total_points = F("total_points") + serializer.data['value']
            points.student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

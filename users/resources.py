from django.http.response import Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Student, Prize, Task, Point
from users.serializers import StudentSerializer, PrizeSerializer, TaskSerializer, PointSerializer


class StudentsResource(APIView):
    def get(self, request, pk=None):
        if pk is None:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
        else:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        Student.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class PointResource(APIView):
    def post(self, request, pk=None):
        serializer = PointSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointDetail(APIView):
        def get_object(self, pk):
            try:
                return Point.objects.get(pk=pk)
            except Point.DoesNotExist:
                raise Http404
        
        def get(self, request, pk, point_pk, format=None):
            point = self.get_object(pk=self.kwargs.get('point_pk', ''))
            serializer = PointSerializer(point)
            return Response(serializer.data)

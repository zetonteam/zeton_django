from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Student, Prize
from users.serializers import StudentSerializer, PrizeSerializer


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

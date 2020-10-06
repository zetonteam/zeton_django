from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Student, Prize


class StudentSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    total_points = serializers.IntegerField()


class StudentsResource(APIView):

    def get(self, request, pk=None):
        if pk is None:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
        else:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
        return Response(serializer.data)


class PrizeSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()


class PrizesResource(APIView):

    def get(self, request, pk=None):
        if pk is None:
            prizes = Prize.objects.all()
            serializer = PrizeSerializer(prizes, many=True)
        else:
            prize = Prize.objects.get(pk=pk)
            serializer = PrizeSerializer(prize)
        return Response(serializer.data)

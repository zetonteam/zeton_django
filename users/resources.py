from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Student


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


@api_view(["GET"])
def students_resource(request, pk=None):
    if pk is None:
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
    else:
        student = Student.objects.get(pk=pk)
        serializer = StudentSerializer(student)
    return Response(serializer.data)

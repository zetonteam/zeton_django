from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import (
    NotAuthenticated,
    APIException,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Caregiver, Student, Prize, Task, Point
from .permissions import HasUserAccessToStudent, IsUserCaregiver

from .serializers import (
    CustomUserSerializer,
    CustomUserSerializerWithToken,
    StudentSerializer,
    PrizeSerializer,
    TaskSerializer,
    PointSerializer,
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


class _NotFoundOrPermissionDenied(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found or permission denied."
    default_code = "not_found_or_permission_denied"


class _CustomAPIView(APIView):
    """
    Modified 'APIView'.
    Throws 'NotFound' exception when permission is denied.
    """

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        - 'NotAuthenticated' when user is not authenticated.
        - 'NotFound' when permission is denied.
        """
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated()
        raise _NotFoundOrPermissionDenied()

    def get_object(self, model_type, **kwargs):
        """
        Return object or raise 404.
        Replacement for 'get_object_or_404', but with consistent error message.
        """
        try:
            return model_type.objects.get(**kwargs)

        except model_type.DoesNotExist:
            raise _NotFoundOrPermissionDenied()


class StudentsResource(_CustomAPIView):
    """
    Access students assigned to current user.
    User must be authenticated and must be a caregiver.

    Adding a new student automatically assigns it to current user.
    """

    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserCaregiver]

    def get(self, request):
        caregiver = self.get_object(Caregiver, user_id=request.user.id)
        students = caregiver.students.all()
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)

    def post(self, request):
        # Create new student entry.
        caregiver = self.get_object(Caregiver, user_id=request.user.id)
        student_serializer = StudentSerializer(data=request.data)
        student_serializer.is_valid(raise_exception=True)
        student_serializer.save()

        # Add a role.
        role_data = {
            "role_name": "caregiver",
            "caregiver": caregiver.id,
            "student": student_serializer.data["pk"],
        }
        role_serializer = RoleSerializer(data=role_data)
        role_serializer.is_valid(raise_exception=True)
        role_serializer.save()

        return Response(student_serializer.data)


class SingleStudentResource(_CustomAPIView):
    """
    Access single student assigned to current user.
    User must be authenticated and must be assigned to the accessed student.
    """

    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id):
        student = self.get_object(Student, pk=student_id)
        serializer = StudentSerializer(student)

        return Response(serializer.data)

    def patch(self, request, student_id):
        student = self.get_object(Student, pk=student_id)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PrizesResource(_CustomAPIView):
    """
    Access prizes assigned to the student.
    User must be authenticated and must be assigned to the accessed student.
    """

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


class SinglePrizeResource(_CustomAPIView):
    """
    Access single prize assigned to the student.
    User must be authenticated and must be assigned to the accessed student.
    """

    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id, prize_id):
        prize = self.get_object(Prize, pk=prize_id, student_id=student_id)
        serializer = PrizeSerializer(prize)

        return Response(serializer.data)

    def patch(self, request, student_id, prize_id):
        prize = self.get_object(Prize, pk=prize_id, student_id=student_id)
        serializer = PrizeSerializer(prize, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, student_id, prize_id):
        prize = self.get_object(Prize, pk=prize_id, student_id=student_id)
        prize.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TasksResource(_CustomAPIView):
    """
    Access tasks assigned to the student.
    User must be authenticated and must be assigned to the accessed student.
    """

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


class SingleTaskResource(_CustomAPIView):
    """
    Access single task assigned to the student.
    User must be authenticated and must be assigned to the accessed student.
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id, task_id):
        task = self.get_object(Task, pk=task_id, student_id=student_id)
        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def patch(self, request, student_id, task_id=None):
        task = self.get_object(Task, pk=task_id, student_id=student_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, student_id, task_id=None):
        task = self.get_object(Task, pk=task_id, student_id=student_id)
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PointResource(_CustomAPIView):
    """
    Access points assigned to the student.
    This means claimed prizes and task rewards.
    User must be authenticated and must be assigned to the accessed student.
    """

    permission_classes = [permissions.IsAuthenticated, HasUserAccessToStudent]

    def get(self, request, student_id):
        points = Point.objects.filter(student_id=student_id).order_by(
            "-assignment_date"
        )
        serializer = PointSerializer(points, many=True)

        return Response(serializer.data)

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

        # Update student with new total points.
        new_total_points = student.total_points + total_points_diff
        student_data = {"total_points": new_total_points}
        student_serializer = StudentSerializer(student, data=student_data, partial=True)
        student_serializer.is_valid(raise_exception=True)
        student_serializer.save()

        # Add new Point.
        point_serializer = PointSerializer(
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
        point_serializer.is_valid(raise_exception=True)
        point_serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=point_serializer.data)

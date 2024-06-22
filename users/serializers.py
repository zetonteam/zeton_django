from rest_framework import serializers

from users.models import CustomUser, Point, Prize, Student, Task


class StudentSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    total_points = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create(**user_data)

        return Student.objects.create(
            user=user, total_points=validated_data["total_points"]
        )

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.get("user", {})
        user.email = user_data.get("email", user.email)
        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()

        instance.total_points = validated_data.get(
            "total_points", instance.total_points
        )
        instance.save()
        return instance


class PrizeSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    student = serializers.CharField(source="student.id", read_only=True)
    name = serializers.CharField()
    value = serializers.IntegerField()

    def create(self, validated_data):
        return Prize.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.student = validated_data.get("student", instance.student)
        instance.name = validated_data.get("name", instance.name)
        instance.value = validated_data.get("value", instance.value)
        instance.save()
        return instance


class TaskSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    value = serializers.IntegerField()

    def create(self, validated_data):
        student_id = validated_data.pop("student_id")
        return Task.objects.create(
            student=Student.objects.get(pk=student_id), **validated_data
        )

    def update(self, instance, validated_data):
        instance.student = validated_data.get("student", instance.student)
        instance.name = validated_data.get("name", instance.name)
        instance.value = validated_data.get("value", instance.value)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username")


class CustomUserSerializerWithToken(serializers.ModelSerializer):  # Handling Register
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ("token", "username", "password")


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = (
            "pk",
            "value",
            "assigner",
            "student",
            "assignment_date",
            "points_type",
        )

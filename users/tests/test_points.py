import json
import pytest

from users.models import Point, CustomUser, Student, Caregiver


@pytest.mark.django_db
def test_add_point(client):
    points = Point.objects.all()
    assert len(points) == 0

    response = client.post(
        "/api/users/points/",
        {
            "value": 1,
            "assigner": 1,
            "assignee": 2,
        },
        content_type="application/json"
    )
    assert response.status_code == 201
    assert response.data["value"] == 1
    
    points = Point.objects.all()
    assert len(points) == 1

@pytest.mark.django_db
def test_add_point_invalid_json(client):
    points = Point.objects.all()
    assert len(points) == 0
    
    response = client.post(
        "/api/users/points/",
        {},
        content_type="application/json"
    )
    assert response.status_code == 400
    
    points = Point.objects.all()
    assert len(points) == 0

@pytest.mark.django_db
def test_add_point_invalid_json_keys(client):
    points = Point.objects.all()
    assert len(points) == 0
    
    response = client.post(
        "/api/users/points/",
        {
            "value": 1,
            "assignee": 2,  
        },
        content_type="application/json"
    )
    assert response.status_code == 400
    
    points = Point.objects.all()
    assert len(points) == 0
    
@pytest.mark.django_db
def test_get_single_point(client):
    assigner =  Caregiver.objects.get(pk=1)
    assignee = Student.objects.get(pk=2)
    point = Point.objects.create(value=22, assigner=assigner, assignee=assignee)

    response = client.get(f"/api/users/points/{point.pk}/")

    assert response.status_code == 200
    assert response.data["value"] == 22
    
def test_get_single_point_incorrect_id(client):
    response = client.get(f"/api/users/students/2/points/foo")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_points_for_filtered_student(client):
    caregiver =  Caregiver.objects.get(pk=1)
    requested_student = Student.objects.get(pk=2)
    other_student = Student.objects.get(pk=1)

    point_1 = Point.objects.create(value=22, assigner=caregiver, assignee=requested_student)
    point_2 = Point.objects.create(value=17, assigner=caregiver, assignee=requested_student)
    point_3 = Point.objects.create(value=144, assigner=caregiver, assignee=other_student)

    response = client.get(f"/api/users/points/?studentId=2")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["value"] == 22
    assert response.data[1]["value"] == 17

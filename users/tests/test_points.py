import json
import pytest

from users.models import Point, CustomUser, Student, Caregiver


@pytest.mark.django_db
def test_add_point(client):
    points = Point.objects.all()
    assert len(points) == 0

    response = client.post(
        "/api/users/students/2/points/",
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
        "/api/users/students/2/points/",
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
        "/api/users/students/2/points/",
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

    response = client.get(f"/api/users/students/{assignee.pk}/points/{point.pk}/")

    assert response.status_code == 200
    assert response.data["value"] == 22
    
def test_get_single_point_incorrect_id(client):
    response = client.get(f"/api/users/students/2/points/foo")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_points_for_filtered_student(client):
    assigner =  Caregiver.objects.get(pk=1)
    assignee = Student.objects.get(pk=2)
    point_1 = Point.objects.create(value=22, assigner=assigner, assignee=assignee)
    point_2 = Point.objects.create(value=17, assigner=assigner, assignee=assignee)

    response = client.get(f"/api/users/points/?userId={assignee.pk}")

    assert response.status_code == 200
    assert response.data[0]["value"] == 22
    assert response.data[1]["value"] == 17
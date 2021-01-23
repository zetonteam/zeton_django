import json
import pytest

from users.models import Point, CustomUser, Student


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
        {
            "value": 1,
            "assigner": 0,
            "assignee": 2,  
        },
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
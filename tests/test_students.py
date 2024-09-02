import random
from string import ascii_letters
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestStudents(TestCase):
    """
    Tests for '/api/students/' endpoint.
    """

    def setUp(self):
        self.client = APIClient()

    def test_Get_Success(self):
        # Obtain token.
        token_data = {"username": "opiekun1", "password": "opiekun1"}
        token_response = self.client.post("/api/token-auth/", token_data)
        token = token_response.json()["access"]

        # Access API.
        response = self.client.get(
            "/api/students/", HTTP_AUTHORIZATION="Bearer " + token
        )

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, list)

        # Fixture specific assertions.
        assert len(response_json) == 1
        entry = response_json[0]
        assert "pk" in entry and entry["pk"] == 2
        assert "email" in entry and entry["email"] == "kuba-zeton@mailinator.com"
        assert "username" in entry and entry["username"] == "student1"
        assert "first_name" in entry and entry["first_name"] == "Kuba"
        assert "last_name" in entry and entry["last_name"] == ""
        assert "total_points" in entry and entry["total_points"] == 120

    def test_Get_NoToken(self):
        # Access API.
        response = self.client.get("/api/students/")

        # Assertions.
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"] == "Authentication credentials were not provided."
        )

    def test_Get_InvalidToken(self):
        # Obtain random data of the same length as token.
        def random_text(length):
            return "".join(random.choice(ascii_letters) for _ in range(length))

        bogus_token = random_text(228)

        # Access API.
        response = self.client.get(
            "/api/students/", HTTP_AUTHORIZATION="Bearer " + bogus_token
        )

        # Assertions.
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 3
        assert "detail" in response_json
        assert "code" in response_json
        assert "messages" in response_json

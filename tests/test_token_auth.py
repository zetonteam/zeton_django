from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestTokenAuth(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_Post_Success(self):
        data = {"username": "opiekun1", "password": "opiekun1"}

        response = self.client.post("/api/token-auth/", data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 2
        assert "refresh" in response_json
        assert "access" in response_json

    def test_Post_InvalidUsername(self):
        data = {"username": "asdf", "password": "asdf"}

        response = self.client.post("/api/token-auth/", data=data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "No active account found with the given credentials"
        )

    def test_Post_InvalidPassword(self):
        data = {"username": "opiekun1", "password": "asdf"}

        response = self.client.post("/api/token-auth/", data=data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "No active account found with the given credentials"
        )

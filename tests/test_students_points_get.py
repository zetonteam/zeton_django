from django.test import TestCase
from rest_framework.test import APIClient


class TestStudentsPointsGet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_Post_Success(self):
        data = {"username": "opiekun1", "password": "opiekun1"}

        resp = self.client.post("/api/token-auth/", data=data, format="json")

        assert resp.status_code == 200
        assert resp.headers["Content-Type"] == "application/json"
        resp_json = resp.json()
        assert len(resp_json) == 2
        assert "refresh" in resp_json
        assert "access" in resp_json

    def test_Post_InvalidUsername(self):
        data = {"username": "asdf", "password": "asdf"}

        resp = self.client.post("/api/token-auth/", data=data, format="json")

        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"
        resp_json = resp.json()
        assert len(resp_json) == 1
        assert "detail" in resp_json
        assert (
            resp_json["detail"] == "No active account found with the given credentials"
        )

    def test_Post_InvalidPassword(self):
        data = {"username": "opiekun1", "password": "asdf"}

        resp = self.client.post("/api/token-auth/", data=data, format="json")

        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"
        resp_json = resp.json()
        assert len(resp_json) == 1
        assert "detail" in resp_json
        assert (
            resp_json["detail"] == "No active account found with the given credentials"
        )

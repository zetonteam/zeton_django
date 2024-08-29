from django.test import TestCase
from rest_framework.test import APIClient


class TestCurrentUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_Credentials_Not_Provided(self):
        resp = self.client.get("/api/current-user/")

        assert resp.status_code == 401
        assert resp.headers["Content-Type"] == "application/json"
        resp_json = resp.json()
        assert len(resp_json) == 1
        assert "detail" in resp_json
        assert resp_json["detail"] == "Authentication credentials were not provided."

from rest_framework import status
from .common import EndpointTestCase


class TestTokenAuthPost(EndpointTestCase):
    """
    Tests for '/api/token-auth/' POST endpoint.
    """

    # Endpoint URL.
    VALID_URL = "/api/token-auth/"

    def test_Success(self):
        data = {"username": "opiekun1", "password": "opiekun1"}

        response = self.post(self.VALID_URL, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 2
        assert "refresh" in response_json
        assert "access" in response_json

    def test_InvalidUsername(self):
        data = {"username": "asdf", "password": "asdf"}

        response = self.post(self.VALID_URL, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "No active account found with the given credentials"
        )

    def test_InvalidPassword(self):
        data = {"username": "opiekun1", "password": "asdf"}

        response = self.post(self.VALID_URL, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "No active account found with the given credentials"
        )

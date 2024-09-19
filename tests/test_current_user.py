from rest_framework import status
from .common import EndpointTestCase


class TestCurrentUserGet(EndpointTestCase):
    """
    Tests for '/api/current-user/' GET endpoint.
    """

    # Endpoint URL.
    VALID_URL = "/api/current-user/"

    def test_Success(self):
        # Access API.
        response = self.get(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 2
        assert "id" in response_json
        assert "username" in response_json

        # Fixture specific assertions.
        assert response_json["id"] == 3
        assert response_json["username"] == "opiekun1"

    def test_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)

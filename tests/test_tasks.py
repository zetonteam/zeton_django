from rest_framework import status
from .common import EndpointTestCase


class TestTaskPost(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/tasks/' [POST] endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/tasks/"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/tasks/"
    # Fixture specific URL to invalid student ID.
    STUDENT_NOT_FOUND_URL = "/api/students/12345/tasks/"
    DATA_JSON_POST = {
        "name": "Another new task to do",
        "value": 21,
    }

    def test_Success(self):
        # Send POST data and response HTTPResponse:
        response = self.post(
            self.VALID_URL, data=self.DATA_JSON_POST, token=self.access_token()
        )

        # Basic asserts of Header and status:
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

        response_json = response.json()
        assert isinstance(response_json, dict)

        assert response_json["name"] == "Another new task to do"
        assert response_json["value"] == 21

    def test_Forbidden(self):
        response = self.post(
            self.NOT_PERMITTED_URL, data=self.DATA_JSON_POST, token=self.access_token()
        )
        self.assert_forbidden(response)

    def test_StudentNotFound(self):
        response = self.post(
            self.STUDENT_NOT_FOUND_URL,
            data=self.DATA_JSON_POST,
            token=self.access_token(),
        )
        self.assert_not_found(response)

    def test_TaskNotFound(self):
        response = self.post(
            self.STUDENT_NOT_FOUND_URL,
            data=self.DATA_JSON_POST,
            token=self.access_token(),
        )
        # TODO: This test provides results are not caught by 'self.assert_not_found'.
        # TODO: This is actually more expected result.
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        # assert response_json["detail"] == "No Task matches the given query."
        assert (
            response_json["detail"]
            == "You do not have permission to perform this action."
        )

    def test_NoToken(self):
        response = self.client.post(self.VALID_URL, data=self.DATA_JSON_POST)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.post(
            endpoint_url=self.VALID_URL,
            data=self.DATA_JSON_POST,
            token=self.bogus_token(),
        )
        self.assert_invalid_token(response)

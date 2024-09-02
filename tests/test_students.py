from rest_framework import status
from .common import EndpointTestCase


class TestStudents(EndpointTestCase):
    """
    Tests for '/api/students/' endpoint.
    """

    def test_Get_Success(self):
        # Access API.
        response = self.client.get(
            "/api/students/", HTTP_AUTHORIZATION="Bearer " + self.access_token()
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
        response = self.client.get("/api/students/")
        self.assert_no_token(response)

    def test_Get_InvalidToken(self):
        response = self.client.get(
            "/api/students/", HTTP_AUTHORIZATION="Bearer " + self.bogus_token()
        )
        self.assert_invalid_token(response)


class TestSingleStudent(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/' endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/"

    def test_Get_Success(self):
        # Access API.
        response = self.client.get(
            self.VALID_URL, HTTP_AUTHORIZATION="Bearer " + self.access_token()
        )

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)

        # Fixture specific assertions.
        assert "pk" in response_json and response_json["pk"] == 2
        assert (
            "email" in response_json
            and response_json["email"] == "kuba-zeton@mailinator.com"
        )
        assert "username" in response_json and response_json["username"] == "student1"
        assert "first_name" in response_json and response_json["first_name"] == "Kuba"
        assert "last_name" in response_json and response_json["last_name"] == ""
        assert "total_points" in response_json and response_json["total_points"] == 120

    def test_Get_Forbidden(self):
        # Access API.
        response = self.client.get(
            self.NOT_PERMITTED_URL, HTTP_AUTHORIZATION="Bearer " + self.access_token()
        )

        # Assertions.
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "You do not have permission to perform this action."
        )

    def test_Get_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_Get_InvalidToken(self):
        response = self.client.get(
            self.VALID_URL, HTTP_AUTHORIZATION="Bearer " + self.bogus_token()
        )
        self.assert_invalid_token(response)

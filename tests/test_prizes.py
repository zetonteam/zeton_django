from rest_framework import status
from .common import EndpointTestCase


class TestPrizes(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prizes/' endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prizes/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prizes/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/prizes/"

    def test_Get_Success(self):
        # Access API.
        response = self.get(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, list)

        # Fixture specific assertions.
        assert len(response_json) == 1
        entry = response_json[0]
        assert entry["pk"] == 2
        assert entry["student"] == "2"
        assert entry["name"] == "1 godzina na basenie"
        assert entry["value"] == 30

    def test_Get_Forbidden(self):
        response = self.get(self.NOT_PERMITTED_URL)
        self.assert_forbidden(response)

    def test_Get_NotFound(self):
        response = self.get(self.NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_Get_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_Get_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)


class TestSinglePrize(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prizes/<int:prize_id>' endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prize/2"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prize/1"
    # Fixture specific URL to invalid student ID.
    STUDENT_NOT_FOUND_URL = "/api/students/12345/prize/1"
    # Fixture specific URL to invalid prize ID.
    PRIZE_NOT_FOUND_URL = "/api/students/2/prize/12345"

    def test_Get_Success(self):
        # Access API.
        response = self.get(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)

        # Fixture specific assertions.
        assert response_json["pk"] == 2
        assert response_json["student"] == "2"
        assert response_json["name"] == "1 godzina na basenie"
        assert response_json["value"] == 30

    def test_Get_Forbidden(self):
        response = self.get(self.NOT_PERMITTED_URL)
        self.assert_forbidden(response)

    def test_Get_StudentNotFound(self):
        response = self.get(self.STUDENT_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_Get_PrizeNotFound(self):
        response = self.get(self.PRIZE_NOT_FOUND_URL)
        # TODO: This test provides results are not caught by 'self.assert_not_found'.
        # TODO: This is actually more expected result.
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert response_json["detail"] == "No Prize matches the given query."

    def test_Get_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_Get_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)

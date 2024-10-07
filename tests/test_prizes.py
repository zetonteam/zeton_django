from rest_framework import status
from .common import EndpointTestCase


class TestPrizesGet(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prizes/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prizes/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prizes/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/prizes/"

    def test_Success(self):
        # Access API.
        response = self.get(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, list)

        # Fixture specific assertions.
        assert len(response_json) == 2
        entry = response_json[0]
        assert entry["pk"] == 2
        assert entry["student"] == "2"
        assert entry["name"] == "1 godzina na basenie"
        assert entry["value"] == 30

    def test_Forbidden(self):
        response = self.get(self.NOT_PERMITTED_URL)
        self.assert_not_found(response)

    def test_NotFound(self):
        response = self.get(self.NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)


class TestPrizesPost(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prizes/' POST endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prizes/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prizes/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/prizes/"

    # Valid prize data.
    VALID_PRIZE_DATA = {"name": "Gry komputerowe", "value": 15}

    def test_Success(self):
        response = self.post(self.VALID_URL, self.VALID_PRIZE_DATA)

        # General assertions.
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["Content-Type"] == "application/json"

        # Fixture specific assertions.
        single_prize_url = "/api/students/2/prize/4/"
        post_op_data = self.get(single_prize_url).json()
        assert post_op_data["student"] == "2"
        assert post_op_data["name"] == "Gry komputerowe"
        assert post_op_data["value"] == 15

    def test_NegativePoints(self):
        # Modify valid data.
        prize_data = self.VALID_PRIZE_DATA.copy()
        prize_data["value"] = -15

        # Access API.
        response = self.post(self.VALID_URL, prize_data)

        # General assertions.
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert "value" in response_json
        assert response_json["value"] == [
            "Ensure this value is greater than or equal to 0."
        ]

    def test_Forbidden(self):
        response = self.post(self.NOT_PERMITTED_URL, self.VALID_PRIZE_DATA)
        self.assert_not_found(response)

    def test_NotFound(self):
        response = self.post(self.NOT_FOUND_URL, self.VALID_PRIZE_DATA)
        self.assert_not_found(response)

    def test_EmptyField(self):
        # Remove content of a field.
        invalid_prize_data = self.VALID_PRIZE_DATA.copy()
        invalid_prize_data["name"] = ""

        # Perform POST operation.
        response = self.post(self.VALID_URL, invalid_prize_data)

        # General assertions.
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert "name" in response_json and response_json["name"] == [
            "This field may not be blank."
        ]

    def test_NoToken(self):
        response = self.client.post(self.VALID_URL, self.VALID_PRIZE_DATA)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.post(self.VALID_URL, self.VALID_PRIZE_DATA, self.bogus_token())
        self.assert_invalid_token(response)


class TestSinglePrizeGet(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prize/<int:prize_id>/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prize/2/"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prize/1/"
    # Fixture specific URL to invalid student ID.
    STUDENT_NOT_FOUND_URL = "/api/students/12345/prize/1/"
    # Fixture specific URL to invalid prize ID.
    PRIZE_NOT_FOUND_URL = "/api/students/2/prize/12345/"

    def test_Success(self):
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

    def test_Forbidden(self):
        response = self.get(self.NOT_PERMITTED_URL)
        self.assert_not_found(response)

    def test_StudentNotFound(self):
        response = self.get(self.STUDENT_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_PrizeNotFound(self):
        response = self.get(self.PRIZE_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)


class TestSinglePrizePatch(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prize/<int:prize_id>/' PATCH endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prize/2/"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prize/1/"
    # Fixture specific URL to invalid student ID.
    STUDENT_NOT_FOUND_URL = "/api/students/12345/prize/1/"
    # Fixture specific URL to invalid prize ID.
    PRIZE_NOT_FOUND_URL = "/api/students/2/prize/12345/"

    def test_Success(self):
        # Get current prize data.
        prize_data = self.get(self.VALID_URL).json()

        # Modify prize data.
        prize_data["name"] = "Jazda konna"
        prize_data["value"] = 50

        # Perform PATCH operation.
        response = self.patch(self.VALID_URL, data=prize_data)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

        # Get current prize data and check if modified properly.
        post_patch_response = self.get(self.VALID_URL)
        post_patch_data = post_patch_response.json()
        # Compare data.
        assert prize_data == post_patch_data

    def test_NegativePoints(self):
        # Get current prize data.
        prize_data = self.get(self.VALID_URL).json()

        # Modify prize data.
        prize_data["value"] = -15

        # Perform PATCH operation.
        response = self.patch(self.VALID_URL, data=prize_data)

        # General assertions.
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert "value" in response_json
        assert response_json["value"] == [
            "Ensure this value is greater than or equal to 0."
        ]

    def test_Forbidden(self):
        response = self.patch(self.NOT_PERMITTED_URL, "")
        self.assert_not_found(response)

    def test_StudentNotFound(self):
        response = self.patch(self.STUDENT_NOT_FOUND_URL, "")
        self.assert_not_found(response)

    def test_PrizeNotFound(self):
        response = self.patch(self.PRIZE_NOT_FOUND_URL, "")
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.patch(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.patch(self.VALID_URL, "", self.bogus_token())
        self.assert_invalid_token(response)


class TestSinglePrizeDelete(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/prize/<int:prize_id>/' DELETE endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/prize/2/"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/prize/1/"
    # Fixture specific URL to invalid student ID.
    STUDENT_NOT_FOUND_URL = "/api/students/12345/prize/1/"
    # Fixture specific URL to invalid prize ID.
    PRIZE_NOT_FOUND_URL = "/api/students/2/prize/12345/"

    def test_Success(self):
        # Access API.
        response = self.delete(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.headers["Content-Length"] == "0"

        # Try to GET.
        get_response = self.get(self.VALID_URL)
        self.assert_not_found(get_response)

    def test_Forbidden(self):
        response = self.delete(self.NOT_PERMITTED_URL)
        self.assert_not_found(response)

    def test_StudentNotFound(self):
        response = self.delete(self.STUDENT_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_PrizeNotFound(self):
        response = self.delete(self.PRIZE_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.delete(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.delete(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)

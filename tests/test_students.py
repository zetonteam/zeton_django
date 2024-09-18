from rest_framework import status
from .common import EndpointTestCase


class TestStudentsGet(EndpointTestCase):
    """
    Tests for '/api/students/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/"

    def test_Success(self):
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
        assert "pk" in entry and entry["pk"] == 2
        assert "email" in entry and entry["email"] == "kuba-zeton@mailinator.com"
        assert "username" in entry and entry["username"] == "student1"
        assert "first_name" in entry and entry["first_name"] == "Kuba"
        assert "last_name" in entry and entry["last_name"] == ""
        assert "total_points" in entry and entry["total_points"] == 120

    def test_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)


class TestStudentsPost(EndpointTestCase):
    """
    Tests for '/api/students/' POST endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/"

    # Valid student data.
    VALID_DATA = {
        "email": "user@example.com",
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "total_points": 321,
    }

    def test_Success(self):
        # Access API.
        response = self.post(self.VALID_URL, self.VALID_DATA)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

        # Fixture specific assertions.
        single_student_url = "/api/students/3/"
        post_op_data = self.get(single_student_url).json()
        assert post_op_data["email"] == "user@example.com"
        assert post_op_data["username"] == "test_username"
        assert post_op_data["first_name"] == "test_first_name"
        assert post_op_data["last_name"] == "test_last_name"
        assert post_op_data["total_points"] == 321

    def test_NoToken(self):
        response = self.client.post(self.VALID_URL, self.VALID_DATA)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.post(self.VALID_URL, self.VALID_DATA, self.bogus_token())
        self.assert_invalid_token(response)


class TestSingleStudentGet(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/"

    def test_Get_Success(self):
        # Access API.
        response = self.get(self.VALID_URL)

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


class TestSingleStudentPatch(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/' PATCH endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/"

    def test_Success(self):
        # Get current student data.
        student_data = self.get(self.VALID_URL).json()

        # Modify student data.
        student_data["email"] = "new-mail@mailinator.com"
        student_data["username"] = "new-username"
        student_data["first_name"] = "John"
        student_data["last_name"] = "Doe"

        # Perform PATCH operation.
        response = self.patch(self.VALID_URL, student_data)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

        # Get current student data and check if modified properly.
        post_patch_response = self.get(self.VALID_URL)
        post_patch_data = post_patch_response.json()
        # Compare data.
        assert student_data == post_patch_data

    def test_EmptyField(self):
        # Get current student data.
        student_data = self.get(self.VALID_URL).json()

        # Modify student data.
        student_data["last_name"] = ""

        # Perform PATCH operation.
        response = self.patch(self.VALID_URL, student_data)

        # General assertions.
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert "last_name" in response_json and response_json["last_name"] == [
            "This field may not be blank."
        ]

    def test_Forbidden(self):
        response = self.patch(self.NOT_PERMITTED_URL, "")
        self.assert_forbidden(response)

    def test_NotFound(self):
        response = self.patch(self.NOT_FOUND_URL, "")
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.patch(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.patch(self.VALID_URL, "", self.bogus_token())
        self.assert_invalid_token(response)

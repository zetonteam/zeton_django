from rest_framework import status
from .common import EndpointTestCase


class TestTasksGet(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/tasks/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/tasks/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/tasks/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/tasks/"

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
        assert entry["pk"] == 2
        assert entry["name"] == "Podlanie kwiatów"
        assert entry["value"] == 1

    def test_Forbidden(self):
        response = self.get(self.NOT_PERMITTED_URL)
        self.assert_forbidden(response)

    def test_NotFound(self):
        response = self.get(self.NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)


class TestTasksPost(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/tasks/' POST endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/tasks/"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/tasks/"
    # Fixture specific URL to invalid student ID.
    TASK_NOT_FOUND_URL = "/api/students/12345/tasks/"

    # Valid task data.
    VALID_JSON_TASK_POST = {
        "name": "Another new task to do",
        "value": 21,
    }

    def test_Success(self):
        # Send POST data and response HTTPResponse:
        response = self.post(self.VALID_URL, data=self.VALID_JSON_TASK_POST)

        # General assertions.
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["Content-Type"] == "application/json"

        # Fixture specific assertions.
        single_task_url = "/api/students/2/task/3/"
        post_op_data = self.get(single_task_url).json()
        assert post_op_data["name"] == "Another new task to do"
        assert post_op_data["value"] == 21

    def test_Forbidden(self):
        response = self.post(self.NOT_PERMITTED_URL, self.VALID_JSON_TASK_POST)
        self.assert_forbidden(response)

    def test_NotFound(self):
        response = self.post(self.TASK_NOT_FOUND_URL, self.VALID_JSON_TASK_POST)
        self.assert_not_found(response)

    def test_EmptyField(self):
        # Remove content of a field.
        invalid_prize_data = self.VALID_JSON_TASK_POST.copy()
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
        response = self.client.post(self.VALID_URL, self.VALID_JSON_TASK_POST)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.post(
            self.VALID_URL, self.VALID_JSON_TASK_POST, self.bogus_token()
        )
        self.assert_invalid_token(response)


class TestSingleTaskGet(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/task/<int:task_id>/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/task/2/"
    # Fixture specific URL to student data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/task/1/"
    # Fixture specific URL to invalid student ID.
    STUDENT_NOT_FOUND_URL = "/api/students/12345/task/1/"
    # Fixture specific URL to invalid task ID.
    TASK_NOT_FOUND_URL = "/api/students/2/task/12345/"

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
        assert response_json["name"] == "Podlanie kwiatów"
        assert response_json["value"] == 1

    def test_Forbidden(self):
        response = self.get(self.NOT_PERMITTED_URL)
        self.assert_forbidden(response)

    def test_StudentNotFound(self):
        response = self.get(self.STUDENT_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_TaskNotFound(self):
        response = self.get(self.TASK_NOT_FOUND_URL)
        # TODO: This test provides results are not caught by 'self.assert_not_found'.
        # TODO: This is actually more expected result.
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert response_json["detail"] == "No Task matches the given query."

    def test_NoToken(self):
        response = self.client.get(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.get(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)

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
        assert entry["student"] == "2"
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
        assert response_json["student"] == "2"
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


class TestSingleTaskPatch(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/task/<int:task_id>/' PATCH endpoint.
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
        # Get current task data.
        task_data = self.get(self.VALID_URL).json()

        # Modify task data.
        task_data["name"] = "Umycie zębów"
        task_data["value"] = 6

        # Access API.
        response = self.patch(self.VALID_URL, task_data)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

        # Get current task data and check if modified properly.
        post_patch_response = self.get(self.VALID_URL)
        post_patch_data = post_patch_response.json()
        # Compare data.
        assert task_data == post_patch_data

    def test_NegativePoints(self):
        # Get current task data.
        task_data = self.get(self.VALID_URL).json()

        # Modify task data.
        task_data["value"] = -15

        # Perform PATCH operation.
        response = self.patch(self.VALID_URL, data=task_data)

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
        self.assert_forbidden(response)

    def test_StudentNotFound(self):
        response = self.patch(self.STUDENT_NOT_FOUND_URL, "")
        self.assert_not_found(response)

    def test_TaskNotFound(self):
        response = self.patch(self.TASK_NOT_FOUND_URL, "")
        # TODO: This test provides results are not caught by 'self.assert_not_found'.
        # TODO: This is actually more expected result.
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert response_json["detail"] == "No Task matches the given query."

    def test_NoToken(self):
        response = self.client.patch(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.patch(self.VALID_URL, "", self.bogus_token())
        self.assert_invalid_token(response)


class TestSingleTaskDelete(EndpointTestCase):
    """
    Tests for '/api/students/<int:student_id>/task/<int:task_id>/' DELETE endpoint.
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
        response = self.delete(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.headers["Content-Length"] == "0"

        # Try to GET.
        get_response = self.get(self.VALID_URL)
        # TODO: This test provides results are not caught by 'self.assert_not_found'.
        # TODO: This is actually more expected result.
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        assert get_response.headers["Content-Type"] == "application/json"
        response_json = get_response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert response_json["detail"] == "No Task matches the given query."

    def test_Forbidden(self):
        response = self.delete(self.NOT_PERMITTED_URL)
        self.assert_forbidden(response)

    def test_StudentNotFound(self):
        response = self.delete(self.STUDENT_NOT_FOUND_URL)
        self.assert_not_found(response)

    def test_TaskNotFound(self):
        response = self.delete(self.TASK_NOT_FOUND_URL)
        # TODO: This test provides results are not caught by 'self.assert_not_found'.
        # TODO: This is actually more expected result.
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert response_json["detail"] == "No Task matches the given query."

    def test_NoToken(self):
        response = self.client.delete(self.VALID_URL)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.delete(self.VALID_URL, self.bogus_token())
        self.assert_invalid_token(response)

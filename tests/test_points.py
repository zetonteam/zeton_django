from rest_framework import status
from .common import EndpointTestCase


class TestPointsGet(EndpointTestCase):
    """
    Test for '/api/students/<int:student_id>/points/' GET endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/points/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/points/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/points/"

    def test_Success(self):
        # Access API.
        response = self.get(self.VALID_URL)

        # General assertions.
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert isinstance(response_json, dict)

        # Fixture specific assertions.
        def assert_entry(
            recv_point,
            expected_pk,
            expected_value,
            expected_assigner,
            expected_student,
            expected_points_type,
            expected_content_type,
            expected_object_id,
        ):
            assert recv_point["pk"] == expected_pk
            assert recv_point["value"] == expected_value
            assert recv_point["assigner"] == expected_assigner
            assert recv_point["student"] == expected_student
            assert "assignment_date" in recv_point
            assert recv_point["points_type"] == expected_points_type
            assert recv_point["content_type"] == expected_content_type
            assert recv_point["object_id"] == expected_object_id

        assert response_json["count"] == 6
        # TODO: what are 'previous' and 'next' fields for?
        results = response_json["results"]
        # Only first two entries are now tested.
        assert_entry(
            results[0],
            expected_pk=11,
            expected_value=1,
            expected_assigner=1,
            expected_student=2,
            expected_points_type="task",
            expected_content_type=10,
            expected_object_id=2,
        )
        assert_entry(
            results[1],
            expected_pk=10,
            expected_value=30,
            expected_assigner=1,
            expected_student=2,
            expected_points_type="prize",
            expected_content_type=11,
            expected_object_id=2,
        )

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


class TestPointsPost(EndpointTestCase):
    """
    Test for '/api/students/<int:student_id>/points/' POST endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/points/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/points/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/points/"
    # Fixture specific valid data to post a prize.
    VALID_POST_PRIZE = {"content_type": "prize", "object_id": "2"}
    # Fixture specific valid data to post a task.
    VALID_POST_TASK = {"content_type": "task", "object_id": "2"}
    # Fixture specific data to post an invalid content type.
    INVALID_POST_TYPE = {"content_type": "asdf", "object_id": "1"}

    def test_Prize_Success(self):
        response = self.post(self.VALID_URL, self.VALID_POST_PRIZE)
        assert response.status_code == status.HTTP_201_CREATED
        # Fixture specific assertions.
        response_json = response.json()
        assert response_json["value"] == 30
        assert response_json["assigner"] == 1
        assert response_json["student"] == 2
        assert response_json["points_type"] == "prize"
        assert response_json["content_type"] == 11
        assert response_json["object_id"] == 2

    def test_Task_Success(self):
        response = self.post(self.VALID_URL, self.VALID_POST_TASK)
        assert response.status_code == status.HTTP_201_CREATED
        # Fixture specific assertions.
        response_json = response.json()
        assert response_json["value"] == 1
        assert response_json["assigner"] == 1
        assert response_json["student"] == 2
        assert response_json["points_type"] == "task"
        assert response_json["content_type"] == 10
        assert response_json["object_id"] == 2

    def test_Invalid_Type(self):
        response = self.post(self.VALID_URL, self.INVALID_POST_TYPE)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_Forbidden(self):
        response = self.post(self.NOT_PERMITTED_URL, self.VALID_POST_PRIZE)
        self.assert_forbidden(response)

    def test_NotFound(self):
        response = self.post(self.NOT_FOUND_URL, self.VALID_POST_PRIZE)
        self.assert_not_found(response)

    def test_NoToken(self):
        response = self.client.post(self.VALID_URL, self.VALID_POST_PRIZE)
        self.assert_no_token(response)

    def test_InvalidToken(self):
        response = self.post(self.VALID_URL, self.VALID_POST_PRIZE, self.bogus_token())
        self.assert_invalid_token(response)

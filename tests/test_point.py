from rest_framework import status
from .common import EndpointTestCase


class TestPoint(EndpointTestCase):
    """
    Test for '/api/students/<int:id>/points/' endpoint.
    """

    # Fixture specific URL to available student data.
    VALID_URL = "/api/students/2/points/"
    # Fixture specific URL to data not available for current user.
    NOT_PERMITTED_URL = "/api/students/1/points/"
    # Fixture specific URL to invalid student ID.
    NOT_FOUND_URL = "/api/students/12345/points/"

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

    def test_Get_NotFound(self):
        # Access API.
        response = self.client.get(
            self.NOT_FOUND_URL, HTTP_AUTHORIZATION="Bearer " + self.access_token()
        )

        # Assertions.
        # Result should be the same as for accessing student without rights.
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

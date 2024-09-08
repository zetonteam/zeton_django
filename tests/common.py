"""
Module for common testing utilities.
"""

import random
from string import ascii_letters
from typing import Any
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class EndpointTestCase(TestCase):
    """
    Endpoint test case base class.
    """

    def setUp(self):
        self.client = APIClient()

    def get(self, endpoint_url: str, token: str | None = None):
        """
        Helper method to make a GET request.

        Parameters
        ----------
        endpoint_url : str
            Endpoint URL.
        token : str
            Token to be used. 'self.access_token()' is used if 'None'.
        """
        access_token = token if token is not None else self.access_token()
        return self.client.get(
            endpoint_url, HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

    def patch(self, endpoint_url: str, data: Any, token: str | None = None):
        """
        Helper method to make a PATCH request.
        "json" format is assumed.

        Parameters
        ----------
        endpoint_url : str
            Endpoint URL.
        data : Any
            Data to send.
        token : str | None
            Token to be used. 'self.access_token()' is used if 'None'.
        """
        access_token = token if token is not None else self.access_token()
        return self.client.patch(
            endpoint_url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

    def access_token(self) -> str:
        """
        Get access token.
        """
        # Obtain token.
        token_data = {"username": "opiekun1", "password": "opiekun1"}
        token_response = self.client.post("/api/token-auth/", token_data)
        return token_response.json()["access"]

    def bogus_token(self) -> str:
        """
        Get bogus token - randomly generated invalid token.
        """
        return "".join(random.choice(ascii_letters) for _ in range(228))

    def assert_no_token(self, response) -> None:
        """
        Common set of assertions for no token tests.

        Parameters
        ----------
        response
            Response for a request without token.
        """
        # Assertions.
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"] == "Authentication credentials were not provided."
        )

    def assert_invalid_token(self, response) -> None:
        """
        Common set of assertions for invalid token tests.

        Parameters
        ----------
        response
            Response for a request with invalid token.
        """
        # Assertions.
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 3
        assert "detail" in response_json
        assert "code" in response_json
        assert "messages" in response_json

    def assert_forbidden(self, response) -> None:
        """
        Common set of assertions for forbidden access tests.

        Parameters
        ----------
        response
            Response for a forbidden access request.
        """
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "You do not have permission to perform this action."
        )

    def assert_not_found(self, response) -> None:
        """
        Common set of assertions for not found access tests.

        Parameters
        ----------
        response
            Response for a request with not found access request.
        """
        # Result should be the same as for accessing without rights.
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 1
        assert "detail" in response_json
        assert (
            response_json["detail"]
            == "You do not have permission to perform this action."
        )

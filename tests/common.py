"""
Module for common testing utilities.
"""

import random
from string import ascii_letters
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class EndpointTestCase(TestCase):
    """
    Endpoint test case base class.
    """

    def setUp(self):
        self.client = APIClient()

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
            Response for a request without token.
        """
        # Assertions.
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        response_json = response.json()
        assert len(response_json) == 3
        assert "detail" in response_json
        assert "code" in response_json
        assert "messages" in response_json

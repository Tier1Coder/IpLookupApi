"""
Integration tests for REST API endpoints.

This module contains integration tests for the REST API endpoints of the Django application.
It uses `pytest` as the testing framework and `requests` to make HTTP requests to the API.
"""


import pytest
import requests

BASE_URL: str = "http://localhost:8080"  # TODO: Load dynamically from an environment variable


class TestApi:
    """
    A test suite for REST API endpoints of the Django application.


    Notes:
    - Uses parameterized test cases for better coverage.
    """

    @pytest.mark.parametrize(
        "ip, expected_status, expected_content",
        [
            ("192.0.2.1", 200, list),
            ("invalid-ip", 400, dict),
        ],
    )
    def test_get_ip_tags_json(self, ip: str, expected_status: int, expected_content: type) -> None:
        """
        Test the JSON response from the /ip-tags/{ip} endpoint.
        """
        url = f"{BASE_URL}/ip-tags/{ip}"
        response: requests.Response = requests.get(url)

        assert response.status_code == expected_status

        json_data = response.json()
        assert isinstance(json_data, expected_content)

    @pytest.mark.parametrize(
        "ip, expected_status, expected_content",
        [
            ("192.0.2.1", 200, "table"),
            ("invalid-ip", 400, "h1"),
        ],
    )
    def test_get_ip_tags_report(self, ip: str, expected_status: int, expected_content: str) -> None:
        """
        Test the HTML response from the /ip-tags-report/{ip} endpoint.
        """
        url = f"{BASE_URL}/ip-tags-report/{ip}"
        response: requests.Response = requests.get(url)

        assert response.status_code == expected_status

        content = response.text
        assert expected_content in content

"""
TODO: Implement more tests for additional cases, such as:
- Edge cases with valid but extreme IPs (e.g., "0.0.0.0", "255.255.255.255").
- Stress tests with large payloads or concurrent requests.
"""

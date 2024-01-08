#!/usr/bin/env python3

import unittest
import json
from parameterized import parameterized, parameterized_class
from unittest import mock
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([("google"), ("abc")])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test the 'org' method of GithubOrgClient.

        Args:
            org_name (str): The name of the organization.
            mock_get_json (Mock): Mock object for the 'get_json' method.

        Returns:
            None
        """
        endpoint = f"https://api.github.com/orgs/{org_name}"
        github_client = GithubOrgClient(org_name)
        github_client.org()
        mock_get_json.assert_called_once_with(endpoint)

    @parameterized.expand(
            [("random-url", {"repos_url": "http://some_url.com"})]
    )
    def test_public_repos_url(self, org_name, result):
        """
        Test the '_public_repos_url' property of GithubOrgClient.

        Args:
            org_name (str): The name of the organization.
            result (dict): Dictionary containing results of the 'org' method.

        Returns:
            None
        """
        with patch("client.GithubOrgClient.org",
                   PropertyMock(return_value=result)):
            response = GithubOrgClient(org_name)._public_repos_url
            self.assertEqual(response, result.get("repos_url"))

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test the 'public_repos' method of GithubOrgClient.

        Args:
            mock_get_json (Mock): Mock object for the 'get_json' method.

        Returns:
            None
        """
        repos_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = repos_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            # Set up mock data for the '_public_repos_url' property
            mock_public_repos_url.return_value = "hello, world"

            response = GithubOrgClient("test").public_repos()
            expected_response = [repo["name"] for repo in repos_payload]
            self.assertEqual(response, expected_response)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo_info, license_key, expectation):
        """
        Test the 'has_license' method of GithubOrgClient.

        Args:
            repo_info (dict): Dictionary containing repository information.
            license_key (str): The license key to check for.
            expectation (bool): The expected result of 'has_license' method.

        Returns:
            None
        """
        result = GithubOrgClient.has_license(repo_info, license_key)
        self.assertEqual(result, expectation)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class using parameterized class.

    Attributes:
        org_payload (dict): Mocked organization payload.
        repos_payload (dict): Mocked repositories payload.
        expected_repos (list): Expected list of repositories.
        apache2_repos (list): Expected list of repositories
        with Apache 2.0 license.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method to configure the mock for 'requests.get' method.
        """
        config = {
            "return_value.json.side_effect": [
                cls.org_payload,
                cls.repos_payload,
                cls.org_payload,
                cls.repos_payload,
            ]
        }
        cls.get_patcher = patch("requests.get", **config)
        cls.mock = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method to stop the 'requests.get' patch.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test for fetching public repositories.

        Validates the behavior of the 'public_repos' method in GithubOrgClient.
        """
        client = GithubOrgClient("google")

        self.assertEqual(client.org, self.org_payload)
        self.assertEqual(client.repos_payload, self.repos_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """
        Integration test for fetching public repositories
        with a specific license.

        Validates the behavior of the 'public_repos' method
        with license filtering.
        """
        client = GithubOrgClient("google")

        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("XLICENSE"), [])
        self.assertEqual(client.public_repos("apache-2.0"),
                         self.apache2_repos)
        self.mock.assert_called()

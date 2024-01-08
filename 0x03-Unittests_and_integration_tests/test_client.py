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

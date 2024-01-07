#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


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

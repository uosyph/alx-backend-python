#!/usr/bin/env python3
"""
Module: test_utils.py

This module contains unit tests for the utility functions provided in the
'utils' module. The utility functions include 'access_nested_map', 'get_json',
and the 'memoize' decorator.

The test cases cover various scenarios for each utility function to ensure
their correct behavior.

Tested Functions:
1. access_nested_map: Function for accessing nested paths within dictionaries.
2. get_json: Function for retrieving JSON from specified URLs.
3. memoize: Decorator for memoizing the result of a method to
optimize performance.

Test Classes:
1. 'TestAccessNestedMap': Test case class for 'access_nested_map' function.
   - Tests successful path access and exception handling for invalid paths.

2. 'TestGetJson': Test case class for 'get_json' function.
   - Tests the retrieval of JSON from different URLs.

3. 'TestMemoize': Test case class for 'memoize' decorator.
   - Tests the memoization of a method within a class.
"""

import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case class for the 'access_nested_map' function.

    This class contains test methods to validate the behavior of the
    'access_nested_map' function when accessing nested paths within
    dictionaries. It includes tests for both successful path access and
    the handling of exceptions for invalid paths.
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, map, path, expected_output):
        """
        Test that the 'access_nested_map' function returns the expected output
        when given a map and a nested path.

        Args:
            map (dict): The input dictionary.
            path (tuple): The nested path to access within the dictionary.
            expected_output: The expected output when
            accessing the specified path.

        Returns:
            None: This method asserts the equality of
            the actual and expected outputs.

        Raises:
            AssertionError: If the actual output does not
            match the expected output.
        """
        output = access_nested_map(map, path)
        self.assertEqual(output, expected_output)

    @parameterized.expand([({}, ("a",), "a"), ({"a": 1}, ("a", "b"), "b")])
    def test_access_nested_map_exception(self, map, path, wrong_output):
        """
        Test that the 'access_nested_map' function raises the correct exception
        when given a map and an invalid nested path.

        Args:
            map (dict): The input dictionary.
            path (tuple): The nested path to access within the dictionary.
            wrong_output: The expected exception message.

        Returns:
            None: This method asserts the correctness of the raised exception.

        Raises:
            AssertionError: If the exception message does not
            match the expected message.
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(map, path)
            self.assertEqual(wrong_output, str(e.exception))


class TestGetJson(unittest.TestCase):
    """
    Test case class for the 'get_json' function.

    This class includes test methods to validate the behavior of the
    'get_json' function, which is responsible for retrieving JSON from
    specified URLs. The tests cover different scenarios, ensuring the function
    correctly handles various input cases.
    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(self, test_url, test_payload):
        """
        Test the 'get_json' method.

        Args:
            test_url (str): The URL for testing.
            test_payload (dict): The expected JSON payload.

        Returns:
            None: Asserts the equality of the actual and expected outputs.

        Raises:
            AssertionError: If the actual output does not
            match the expected output.
        """
        # Create a Mock with json method returning test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch 'requests.get' to return the mock_response
        with patch("requests.get", return_value=mock_response):
            response = get_json(test_url)
            self.assertEqual(response, test_payload)
            mock_response.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """
    Test case class for the 'memoize' decorator.

    This class contains a test method to validate the behavior of the 'memoize'
    decorator when applied to a method within a class. It ensures that
    the decorated method is memoized, meaning subsequent calls return the
    cached result without re-computation.
    """

    def test_memoize(self):
        """
        Test the 'memoize' decorator functionality.

        This test method creates a test class with a memoized property and
        verifies that the underlying method is called only once, even when
        the property is accessed multiple times.

        Returns:
            None: Asserts the behavior of the 'memoize' decorator.

        Raises:
            AssertionError: If the expected behavior is not
            observed during testing.
        """

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            spec = TestClass()
            spec.a_property
            spec.a_property
            mocked.asset_called_once()

#!/usr/bin/env python3

import unittest
from utils import access_nested_map
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
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
        real_output = access_nested_map(map, path)
        self.assertEqual(real_output, expected_output)

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

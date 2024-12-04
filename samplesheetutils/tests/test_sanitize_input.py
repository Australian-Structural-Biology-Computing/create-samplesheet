import unittest
from samplesheetutils.utils.input import *

class TestSanitizeInput(unittest.TestCase):
    def test_valid_string(self):
        """
        Tests the sanitize_input function with a valid input string with no substitute characters
        """
        input_data = "ValidString"
        sanitize_output = sanitize_input(input_data)

        self.assertEqual(input_data, sanitize_output)

    def test_invalid_string(self):
        """
        Tests the sanitize_input function with an invalid string with substitutable characters
        """
        input_data = "This,Is.An<Invalid>String'and this;test:will.catch it :3"
        sanitize_output = sanitize_input(input_data)

        invalid_chars = False
        for i in [',', ' ', '<', '>', '.', "'", '"', ';', ':']:
            if i in sanitize_output:
                invalid_chars = True

        self.assertFalse(invalid_chars)


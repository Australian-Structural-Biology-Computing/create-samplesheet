import unittest, os
from samplesheetutils.utils.sample import *

class TestSampleName(unittest.TestCase):
    def test_6_char_input(self):
        """
        Tests the sample_name function with an input greater than 6 characters
        """
        input_data = "MPGAFSQNSSKRRAVLPRSHR"
        sample_name_output = sample_name(input_data)

        self.assertEqual(input_data[:6], sample_name_output)

    def test_2_char_input(self):
        """
        Tests the sample_name function with an input less than 6 characters
        """
        input_data = "MPG"
        sample_name_output = sample_name(input_data)

        self.assertEqual(input_data, sample_name_output)

    def test_exact_6_char_input(self):
        """
        Tests the sample_name function with an input of exactly 6 characters
        """
        input_data = "MPGAFS"
        sample_name_output = sample_name(input_data)

        self.assertEqual(input_data, sample_name_output)


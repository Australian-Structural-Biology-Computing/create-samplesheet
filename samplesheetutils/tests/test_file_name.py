import unittest
from samplesheetutils.utils.sample import *

class TestFileName(unittest.TestCase):
    def test_file_name(self):
        """
        Test file_name function with a valid Sample ID
        """
        sample_id = "AAAAAA"
        file_name_output = file_name(sample_id)

        self.assertEqual(file_name_output, "manual_entry-AAAAAA-af2.fasta")

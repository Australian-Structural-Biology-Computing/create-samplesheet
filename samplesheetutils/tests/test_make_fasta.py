import unittest
from samplesheetutils.utils.fasta import *
from samplesheetutils.utils.sample import *

class TestMakeFasta(unittest.TestCase):
    def test_make_fasta(self):
        """
        Tests make_fasta with a sample input
        """
        sample_input = Sample("TEST", ".tmp.fasta", "AAAAAAA")
        make_fasta(sample_input)

        fp = open(".tmp.fasta", "r")
        fp_data = fp.read()
        fp.close()
        self.assertEqual(fp_data, ">TEST\nAAAAAAA")


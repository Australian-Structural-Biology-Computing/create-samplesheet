import unittest, os
from samplesheetutils.utils.output import *
from samplesheetutils.utils.sample import *
from samplesheetutils.utils.fasta import *

class TestCreateCSV(unittest.TestCase):
    def test_create_csv_single_sample(self):
        """
        Test create_csv with a single sample
        """
        sample_input = Sample("TEST", ".tmp.fasta", "AAAAAA")

        with open(".tmp.csv", "w") as fp:
            create_csv([sample_input], "sample", "sequence", fp)

        fp = open(".tmp.csv", "r")
        fp_data = fp.read()
        fp.close()
        self.assertEqual(fp_data, "sample,sequence\nTEST,.tmp.fasta\n")
        os.remove(".tmp.csv")

    def test_create_csv_multiple_sample(self):
        """
        Test create_csv with multiple samples
        """
        sample_input = []
        sample_input.append(Sample("TEST1", ".tmp1.fasta", "AAAAAA"))
        sample_input.append(Sample("TEST2", ".tmp2.fasta", "AAAAAA"))
        sample_input.append(Sample("TEST3", ".tmp3.fasta", "AAAAAA"))

        with open(".tmp.csv", "w") as fp:
            create_csv(sample_input, "sample", "sequence", fp)

        fp = open(".tmp.csv", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "sample,sequence\nTEST1,.tmp1.fasta\nTEST2,.tmp2.fasta\nTEST3,.tmp3.fasta\n")
        os.remove(".tmp.csv")

    def test_create_csv_with_invalid_sample_name(self):
        """
        Test create_csv with an invalid sample name
        """
        sample_input = Sample("invalid,,,name :3", ".tmp.fasta", "AAAAAA")

        with open(".tmp.csv", "w") as fp:
            create_csv([sample_input], "sample", "sequence", fp)

        fp = open(".tmp.csv", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "sample,sequence\ninvalid___name__3,.tmp.fasta\n")
        os.remove(".tmp.csv")        



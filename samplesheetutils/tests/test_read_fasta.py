import unittest, os
from samplesheetutils.utils.fasta import *

class TestReadFASTA(unittest.TestCase):
    def test_single_sample_fasta(self):
        """
        Tests reading a FASTA file containing a single sample
        """
        # Write FASTA file temporarily
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nMPGAFSQNSSKRRAVLPRSHR")
        fp.close()

        with open(".tmp.fasta", "r") as fasta_fp:
            fasta_output = read_fasta(
                fp=fasta_fp,
                read_data=True,
                single_line=False
            )

        self.assertEqual(len(fasta_output), 1)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "MPGAFSQNSSKRRAVLPRSHR")
        os.remove(".tmp.fasta")

    def test_fixed_width_fasta(self):
        """
        Test reading a FASTA file containing a single fixed-width sample
        """
        # Write FASTA temporarily
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        fp.close()

        with open(".tmp.fasta", "r") as fasta_fp:
            fasta_output = read_fasta(
                fp=fasta_fp,
                read_data=True,
                single_line=False
            )

        self.assertEqual(len(fasta_output), 1)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "A"*160)
        os.remove(".tmp.fasta")

    def test_multimer_sample_fasta(self):
        """
        Test reading a FASTA file containing multiple samples
        """
        # Write FASTA temporarily
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nMPGAFSQNSSKRRAVLPRSHR\n>DEMO\nAAAAAAAAAAAA")
        fp.close()

        with open(".tmp.fasta", "r") as fasta_fp:
            fasta_output = read_fasta(
                fp=fasta_fp,
                read_data=True,
                single_line=False
            )

        self.assertEqual(len(fasta_output), 2)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "MPGAFSQNSSKRRAVLPRSHR")
        self.assertEqual(fasta_output[1].name, "DEMO")
        self.assertEqual(fasta_output[1].data, "AAAAAAAAAAAA")
        os.remove(".tmp.fasta")

    def test_multimer_fixed_width_sample_fasta(self):
        """
        Test reading a FASTA file containing multiple fixed width samples
        """
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nMPGAFSQNSS\nKRRAVLPRSHR\n>DEMO\nAAAAAA\nAAAAAA")
        fp.close()

        with open(".tmp.fasta", "r") as fasta_fp:
            fasta_output = read_fasta(
                fp=fasta_fp,
                read_data=True,
                single_line=False
            )

        self.assertEqual(len(fasta_output), 2)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "MPGAFSQNSSKRRAVLPRSHR")
        self.assertEqual(fasta_output[1].name, "DEMO")
        self.assertEqual(fasta_output[1].data, "AAAAAAAAAAAA")
        os.remove(".tmp.fasta")

    def test_invalid_fasta_file(self):
        """
        Test reading a FASTA file containing invalid content
        """
        fp = open(".tmp.fasta", "w")
        fp.write("!!! CHECK IT OUT. I'M IN THE HOUSE LIKE CARPET !!!\n")
        fp.close()

        with open(".tmp.fasta", "r") as fasta_fp:
            fasta_output = read_fasta(
                fp=fasta_fp,
                read_data=True,
                single_line=False
            )

        self.assertEqual(len(fasta_output), 0)
        os.remove(".tmp.fasta")


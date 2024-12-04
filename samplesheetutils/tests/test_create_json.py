import unittest, json, os
from samplesheetutils.utils.output import *
from samplesheetutils.utils.sample import *

class TestCreateJSON(unittest.TestCase):
    def test_create_json_single_sample(self):
        """
        Test create_json with single sample input
        """
        sample_input = Sample("TEST", ".tmp.fasta", "AAAAAA")

        with open(".tmp.json", "w") as fp:
            create_json([sample_input], fp)

        fp = open(".tmp.json", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "{\"entities\": [{\"type\": \"protein\", \"sequence\": \"AAAAAA\", \"count\": \"1\"}]}")
        os.remove(".tmp.json")

    def test_create_json_multiple_sample(self):
        """
        Test create_json with multiple sample inputs
        """
        sample_input = []
        sample_input.append(Sample("TEST1", ".tmp1.fasta", "AAAAAA"))
        sample_input.append(Sample("TEST2", ".tmp2.fasta", "AAAAAA"))
        sample_input.append(Sample("TEST3", ".tmp3.fasta", "AAAAAA"))

        with open(".tmp.json", "w") as fp:
            create_json(sample_input, fp)

        fp = open(".tmp.json", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, '{"entities": [{"type": "protein", "sequence": "AAAAAA", "count": "1"}, {"type": "protein", "sequence": "AAAAAA", "count": "1"}, {"type": "protein", "sequence": "AAAAAA", "count": "1"}]}')
        os.remove(".tmp.json")

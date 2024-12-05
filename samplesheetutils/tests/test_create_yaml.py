import unittest, yaml, os
from samplesheetutils.utils.output import *
from samplesheetutils.utils.sample import *

class TestCreateYAML(unittest.TestCase):
    def test_create_yaml_single_sample(self):
        sample_input = Sample("TEST", ".tmp.fasta", "AAAAAA")

        with open(".tmp.yaml", "w") as fp:
            create_yaml_boltz([sample_input], fp)

        fp = open(".tmp.yaml", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, 'sequences:\n- protein:\n    id: TEST\n    sequence: AAAAAA\nversion: 1\n')
        os.remove(".tmp.yaml")

    def test_create_yaml_multiple_sample(self):
        sample_input = []
        sample_input.append(Sample("TEST1", ".tmp1.fasta", "AAAAAA"))
        sample_input.append(Sample("TEST2", ".tmp2.fasta", "AAAAAA"))
        sample_input.append(Sample("TEST3", ".tmp3.fasta", "AAAAAA"))

        with open(".tmp.yaml", "w") as fp:
            create_yaml_boltz(sample_input, fp)

        fp = open(".tmp.yaml", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "sequences:\n- protein:\n    id: TEST\n    sequence: AAAAAA\n- protein:\n    id: TEST\n    sequence: AAAAAA\n- protein:\n    id: TEST\n    sequence: AAAAAA\nversion: 1\n")
        os.remove(".tmp.yaml")

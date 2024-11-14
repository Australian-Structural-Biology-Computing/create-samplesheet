import unittest, os
import create_samplesheet

class TestSampleName(unittest.TestCase):
    def test_6_char_input(self):
        """
        Tests the sample_name function with an input greater than 6 characters
        """
        input_data = "MPGAFSQNSSKRRAVLPRSHR"
        sample_name_output = create_samplesheet.sample_name(input_data)

        self.assertEqual(input_data[:6], sample_name_output)

    def test_2_char_input(self):
        """
        Tests the sample_name function with an input less than 6 characters 
        """
        input_data = "MPG"
        sample_name_output = create_samplesheet.sample_name(input_data)

        self.assertEqual(input_data, sample_name_output)
    
    def test_exact_6_char_input(self):
        """
        Tests the sample_name function with an input of exactly 6 characters 
        """
        input_data = "MPGAFS"
        sample_name_output = create_samplesheet.sample_name(input_data)

        self.assertEqual(input_data, sample_name_output)

class TestSanitizeInput(unittest.TestCase):
    def test_valid_string(self):
        """
        Tests the sanitize_input function with a valid input string with no substitute characters
        """
        input_data = "ValidString"
        sanitize_output = create_samplesheet.sanitize_input(input_data)

        self.assertEqual(input_data, sanitize_output)
    
    def test_invalid_string(self):
        """
        Tests the sanitize_input function with an invalid string with substitutable characters 
        """
        input_data = "This,Is.An<Invalid>String'and this;test:will.catch it :3"
        sanitize_output = create_samplesheet.sanitize_input(input_data)

        invalid_chars = False
        for i in [',', ' ', '<', '>', '.', "'", '"', ';', ':']:
            if i in sanitize_output:
                invalid_chars = True

        self.assertFalse(invalid_chars)

class TestReadFASTA(unittest.TestCase):
    def test_single_sample_fasta(self):
        """
        Tests reading a FASTA file containing a single sample 
        """
        # Write FASTA file temporarily
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nMPGAFSQNSSKRRAVLPRSHR")
        fp.close()

        fasta_output = create_samplesheet.read_fasta(
            fp=".tmp.fasta",
            read_data=True,
            single_line=False
        )

        self.assertEqual(len(fasta_output), 1)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "MPGAFSQNSSKRRAVLPRSHR")
    
    def test_fixed_width_fasta(self):
        """
        Test reading a FASTA file containing a single fixed-width sample 
        """
        # Write FASTA temporarily 
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        fp.close()

        fasta_output = create_samplesheet.read_fasta(
            fp=".tmp.fasta",
            read_data=True,
            single_line=False
        )

        self.assertEqual(len(fasta_output), 1)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "A"*160)
    
    def test_multimer_sample_fasta(self):
        """
        Test reading a FASTA file containing multiple samples 
        """
        # Write FASTA temporarily
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nMPGAFSQNSSKRRAVLPRSHR\n>DEMO\nAAAAAAAAAAAA")
        fp.close()

        fasta_output = create_samplesheet.read_fasta(
            fp=".tmp.fasta",
            read_data=True,
            single_line=False
        )

        self.assertEqual(len(fasta_output), 2)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "MPGAFSQNSSKRRAVLPRSHR")
        self.assertEqual(fasta_output[1].name, "DEMO")
        self.assertEqual(fasta_output[1].data, "AAAAAAAAAAAA")
    
    def test_multimer_fixed_width_sample_fasta(self):
        """
        Test reading a FASTA file containing multiple fixed width samples 
        """
        fp = open(".tmp.fasta", "w")
        fp.write(">TEST\nMPGAFSQNSS\nKRRAVLPRSHR\n>DEMO\nAAAAAA\nAAAAAA")
        fp.close()
        
        fasta_output = create_samplesheet.read_fasta(
            fp=".tmp.fasta",
            read_data=True,
            single_line=False
        )

        self.assertEqual(len(fasta_output), 2)
        self.assertEqual(fasta_output[0].name, "TEST")
        self.assertEqual(fasta_output[0].data, "MPGAFSQNSSKRRAVLPRSHR")
        self.assertEqual(fasta_output[1].name, "DEMO")
        self.assertEqual(fasta_output[1].data, "AAAAAAAAAAAA")
    
    def test_invalid_fasta_file(self):
        """
        Test reading a FASTA file containing invalid content 
        """
        fp = open(".tmp.fasta", "w")
        fp.write("!!! CHECK IT OUT. I'M IN THE HOUSE LIKE CARPET !!!\n")
        fp.close()

        fasta_output = create_samplesheet.read_fasta(
            fp=".tmp.fasta",
            read_data=True,
            single_line=False
        )

        self.assertEqual(len(fasta_output), 0)

class TestFileName(unittest.TestCase):
    def test_file_name(self):
        """
        Test file_name function with a valid Sample ID 
        """
        sample_id = "AAAAAA"
        file_name_output = create_samplesheet.file_name(sample_id)

        self.assertEqual(file_name_output, "manual_entry-AAAAAA-af2.fasta")

class TestMakeFasta(unittest.TestCase):
    def test_make_fasta(self):
        """
        Tests make_fasta with a sample input
        """
        sample_input = create_samplesheet.Sample("TEST", ".tmp.fasta", "AAAAAAA")
        create_samplesheet.make_fasta(sample_input)
        
        fp = open(".tmp.fasta", "r")
        fp_data = fp.read()
        fp.close()
        self.assertEqual(fp_data, ">TEST\nAAAAAAA")

class TestCreateCSV(unittest.TestCase):
    def test_create_csv_single_sample(self):
        """
        Test create_csv with a single sample 
        """
        sample_input = create_samplesheet.Sample("TEST", ".tmp.fasta", "AAAAAA")

        with open(".tmp.csv", "w") as fp:
            create_samplesheet.create_csv([sample_input], "sample", "sequence", fp)
        
        fp = open(".tmp.csv", "r")
        fp_data = fp.read()
        fp.close()
        self.assertEqual(fp_data, "sample,sequence\nTEST,.tmp.fasta\n")
    
    def test_create_csv_multiple_sample(self):
        """
        Test create_csv with multiple samples 
        """
        sample_input = [] 
        sample_input.append(create_samplesheet.Sample("TEST1", ".tmp1.fasta", "AAAAAA"))
        sample_input.append(create_samplesheet.Sample("TEST2", ".tmp2.fasta", "AAAAAA"))
        sample_input.append(create_samplesheet.Sample("TEST3", ".tmp3.fasta", "AAAAAA"))

        with open(".tmp.csv", "w") as fp:
            create_samplesheet.create_csv(sample_input, "sample", "sequence", fp)
        
        fp = open(".tmp.csv", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "sample,sequence\nTEST1,.tmp1.fasta\nTEST2,.tmp2.fasta\nTEST3,.tmp3.fasta\n")
    
    def test_create_csv_with_invalid_sample_name(self):
        """
        Test create_csv with an invalid sample name 
        """
        sample_input = create_samplesheet.Sample("invalid,,,name :3", ".tmp.fasta", "AAAAAA")
        
        with open(".tmp.csv", "w") as fp:
            create_samplesheet.create_csv([sample_input], "sample", "sequence", fp)
        
        fp = open(".tmp.csv", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "sample,sequence\ninvalid___name__3,.tmp.fasta\n")

class TestCreateJSON(unittest.TestCase):
    def test_create_json_single_sample(self):
        """
        Test create_json with single sample input 
        """
        sample_input = create_samplesheet.Sample("TEST", ".tmp.fasta", "AAAAAA")

        with open(".tmp.json", "w") as fp:
            create_samplesheet.create_json([sample_input], fp)
        
        fp = open(".tmp.json", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, "{\"entities\": [{\"type\": \"protein\", \"sequence\": \"AAAAAA\", \"count\": \"1\"}]}")
    
    def test_create_json_multiple_sample(self):
        """
        Test create_json with multiple sample inputs 
        """
        sample_input = []
        sample_input.append(create_samplesheet.Sample("TEST1", ".tmp1.fasta", "AAAAAA"))
        sample_input.append(create_samplesheet.Sample("TEST2", ".tmp2.fasta", "AAAAAA"))
        sample_input.append(create_samplesheet.Sample("TEST3", ".tmp3.fasta", "AAAAAA"))

        with open(".tmp.json", "w") as fp:
            create_samplesheet.create_json(sample_input, fp)
        
        fp = open(".tmp.json", "r")
        fp_data = fp.read()
        fp.close()

        self.assertEqual(fp_data, '{"entities": [{"type": "protein", "sequence": "AAAAAA", "count": "1"}, {"type": "protein", "sequence": "AAAAAA", "count": "1"}, {"type": "protein", "sequence": "AAAAAA", "count": "1"}]}')

if __name__ == "__main__":
    unittest.main()
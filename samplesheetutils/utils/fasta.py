from samplesheetutils.utils.sample import Sample
from typing import Union
import re 

def read_fasta(fp, read_data=False, single_line=True):
    """
    Read in a FASTA file and return an array containing sequence data
    read_data: Controls if the amino acid sequences are read into the Sample object
    single_line: Return after reading the first header
    """

    fasta_samples = []

    lines = fp.readlines()

    temp_sample_object = None

    for fasta_line in lines:
        if re.search("^\\>.*$", fasta_line):
            # This is to add support for fixed-width fasta files
            if temp_sample_object is not None:
                fasta_samples.append(temp_sample_object)
            temp_sample_object = Sample(fasta_line[1:].strip(), fp.name, "")
            if single_line:
                break
        elif temp_sample_object is not None:
            temp_sample_object.data += fasta_line.strip()

    if temp_sample_object is not None:
        fasta_samples.append(temp_sample_object)

    fp.close()

    return fasta_samples

def make_fasta(sample: Union[Sample, list], header='>', fixed_width=False, fixed_width_column_count=80):
    """
    Write a FASTA file given a Sample object or a list of Sample objects. The Sample object must contain amino acid data.
    sample: Single Sample object or a list of Samples
    header: The header character for each sample. It is recommended not to change this
    fixed_width: Controls if amino acid data is written with line breaks every n characters, or not
    fixed_width_column_count: Controls how often the amino acid data is broken up
    """
    if type(sample) is not list:
        sample = [sample]

    for si in sample:
        with open(si.path, "w") as fp:
            sample_data = si.data
            if fixed_width:
                sample_data = '\n'.join([sample_data[i:i+fixed_width_column_count] for i in range(0, len(sample_data), fixed_width_column_count)]) 
            fp.write(f"{header}{si.name}\n{sample_data}")
            fp.flush()



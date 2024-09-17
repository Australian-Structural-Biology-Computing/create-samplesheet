#!/usr/bin/python3
import argparse, os, tempfile, json, re

# Consts
MODE_STRING_CSV = 0
MODE_DIR_CSV = 1

class Sample:
    def __init__(self, name, path, data):
        self.name = name
        self.path = path
        self.data = data

def sample_name(aa_seq, seq_chars=6):
    trunc_aa_seq = aa_seq[:min(seq_chars, len(aa_seq))]
    return trunc_aa_seq

def read_fasta(fp):
    fasta_samples = []
    for line in fp:
        if re.search("^. .*$", line):
            fasta_samples.append(Sample(line[2:].strip(), fp.name, None))
    return fasta_samples

def file_name(sample_id, prefix='manual_entry', suffix='af2', delim='-', extension='fasta'):
    return ''.join([prefix, delim, sample_id, delim, suffix, '.', extension]) 

def make_fasta(aa_seq, sample_name, fp, header='>'):
    fp.write(f"{header} {sample_name}\n{aa_seq}")
    fp.flush()

def create_csv(data, header_seq, header_fasta, fp):
    fp.write(f"{header_seq},{header_fasta}\n")
    for row in data:
        fp.write(row.name + "," + row.path + "\n")

    fp.flush()

def create_json(data, fp):
    dict_data = {"entities": []}
    
    for row in data:
        dict_data["entities"].append({"type": "protein"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Create Samplesheet",
        description="Utility to create a samplesheet from directory, or AA string")

    parser.add_argument('-a', '--aa-string', help='Single amino acid string', dest='aa_string')
    parser.add_argument('-d', '--directory', help='Directory containing fasta files', dest='dir')
    parser.add_argument('-p', '--prefix', help='Filename prefix for amino acid strings', dest='aa_prefix', default='manual_entry')
    parser.add_argument('-s', '--suffix', help='Filename suffix for amino acid strings', dest='aa_suffix', default='af2')
    parser.add_argument('-u', '--delim', help='Delimiter in between fields of the amino acid string filename', dest='delim', default='-')
    parser.add_argument('-c', '--seq-chars', help='Number of characters used from the sequence in the filename', dest='seq_chars', default=6)
    parser.add_argument('-o', '--output-file', help='Samplesheet filename', dest='output_file', default='samplesheet.csv')
    parser.add_argument('-x', '--output-extension', help='Extension for string input', default='fasta', dest='output_extension')
    parser.add_argument('-e', '--extension', help='Extension of the files contained in the directory', default='fasta', dest='extension')
    parser.add_argument('-q', '--sequence-header', help='Column name for sequence', default='sequence', dest='seq_header')
    parser.add_argument('-f', '--fasta-header', help='Column name for fasta path', default='fasta', dest='fasta_header')
    parser.add_argument('-j', '--json', help='Output json format instead of csv', action='store_true', dest='json')
    parser.add_argument('-t', '--fasta-dir', help='Output directory for temporary fasta files', default=os.getcwd(), dest='fasta_dir')
    parser.add_argument('-r', '--fasta-match', help='Regex to match for fasta files in directory mode', default='.*\.fa.*$', dest='fasta_regex')

    args = parser.parse_args()

    # Validate that an input was provided
    if (not args.aa_string and not args.dir):
        raise ValueError("You must specify an amino acid string or a directory")

    # Validate that seq_chars is an int
    if (type(args.seq_chars) is not int):
        raise ValueError("seq_chars is not a number")

    # Mode
    mode = 0
    mode |= bool(args.dir)
    mode |= args.json << 1

    if mode == MODE_STRING_CSV:
        # Generate metadata for AA string
        aa_sample_name = sample_name(args.aa_string, seq_chars=args.seq_chars)
        aa_sample_file_name = file_name(aa_sample_name, prefix=args.aa_prefix, suffix=args.aa_suffix, extension=args.output_extension)
        aa_path = args.fasta_dir + "/" + aa_sample_file_name 

        # Create the fasta file
        with open(aa_path, "w") as aa_fp:
            make_fasta(args.aa_string, aa_sample_name, aa_fp)

        sample_data = Sample(aa_sample_name, aa_path, args.aa_string)
       
        # Write the samplesheet 
        samplesheet_path = args.output_file
        with open(samplesheet_path, "w") as ss_fp:
            create_csv([sample_data], args.seq_header, args.fasta_header, ss_fp)

    if mode == MODE_DIR_CSV:
        file_list = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f)) and re.search(args.fasta_regex, f)]         
        sample_data = []

        for file_name in file_list:
            with open(file_name, "r") as file_fp:
                sample_data.extend(read_fasta(file_fp))
        
        samplesheet_path = args.output_file
        with open(samplesheet_path, "w") as ss_fp:
            create_csv(sample_data, args.seq_header, args.fasta_header, ss_fp)

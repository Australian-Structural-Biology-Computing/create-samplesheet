#!/usr/bin/python3
import argparse, os, tempfile, json, re, logging, sys
VERSION="0.4"

# Consts
MODE_STRING_CSV = 0
MODE_DIR_CSV = 1
MODE_STRING_JSON = 2
MODE_DIR_JSON = 3

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig()

class Sample:
    def __init__(self, name, path, data):
        self.name = name
        self.path = path
        self.data = data

def sanitize_input(input_str, disallowed_chars = [',', ' ', '<', '>', '.', "'", '"', ';', ':'], replcement='_'):
    for i in disallowed_chars:
        input_str = input_str.replace(i, '_')
    return input_str

def sample_name(aa_seq, seq_chars=6):
    trunc_aa_seq = aa_seq[:min(seq_chars, len(aa_seq))]
    return trunc_aa_seq

def read_fasta(fp, read_data=False, single_line=True):
    fasta_samples = []
    logger.debug(f"Reading {fp}")

    fasta_fp = open(fp, 'r')
    fasta_fp.seek(0)
    lines = fasta_fp.readlines()
    logger.debug(f"Fasta content {lines}")

    temp_sample_object = None

    for fasta_line in lines:
        if re.search("^\\>.*$", fasta_line):
            # This is to add support for fixed-width fasta files
            logger.debug(f"Found header")
            if temp_sample_object is not None:
                fasta_samples.append(temp_sample_object)
            temp_sample_object = Sample(fasta_line[1:].strip(), fp, "")
            if single_line:
                break
        elif temp_sample_object is not None:
            temp_sample_object.data += fasta_line.strip()
    
    if temp_sample_object is not None:
        fasta_samples.append(temp_sample_object)

    fasta_fp.close()
    logger.debug(f"Number of samples in {fp}: {len(fasta_samples)}")

    return fasta_samples

def file_name(sample_id, prefix='manual_entry', suffix='af2', delim='-', extension='fasta'):
    return ''.join([prefix, delim, sample_id, delim, suffix, '.', extension]) 

def make_fasta(sample : Sample, header='>'):
    with open(sample.path, "w") as fp:
        fp.write(f"{header}{sample.name}\n{sample.data}")
        fp.flush()

def create_csv(data, header_seq, header_fasta, fp):
    fp.write(f"{header_seq},{header_fasta}\n")
    logger.debug(f"Written CSV header {header_seq},{header_fasta}")
    for row in data:
        fp.write(sanitize_input(row.name) + "," + row.path + "\n")
        logger.debug(f"Wrote row for {row.name}")

    fp.flush()

def create_json(data, fp):
    dict_data = {"entities": []}
    
    for row in data:
        dict_data["entities"].append({"type": "protein", "sequence": row.data, "count": "1"})
    
    json.dump(dict_data, fp)
    fp.flush()

def version():
    print(f"create-samplesheet version {VERSION}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Create Samplesheet",
        description="Utility to create a samplesheet from directory, or AA string",
        epilog="Written by Nathan Glades <n.glades@unsw.edu.au>")

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
    parser.add_argument('-r', '--fasta-match', help='Regex to match for fasta files in directory mode', default='.*\.fa(sta)?.*$', dest='fasta_regex')
    parser.add_argument('--monomer', help='Create a samplesheet entry for each sample in a fasta file', default=False, action='store_true', dest='monomer')
    parser.add_argument('--version', help='Show version number', default=False, action='store_true', dest='version')
    parser.add_argument('--debug', help='Show debug output', default=False, action='store_true', dest='debug')

    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if (args.version):
        version()
        exit(0)

    if (args.debug):
        version()

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
    logger.debug(f"mode: {mode}")

    if mode == MODE_STRING_CSV:
        # Generate metadata for AA string
        aa_sample_name = sample_name(args.aa_string, seq_chars=args.seq_chars)
        aa_sample_file_name = file_name(aa_sample_name, prefix=args.aa_prefix, suffix=args.aa_suffix, extension=args.output_extension)
        aa_path = args.fasta_dir + "/" + aa_sample_file_name 

        # Create the fasta file
        sample_data = Sample(aa_sample_name, aa_path, args.aa_string)
        make_fasta(sample_data)
       
        # Write the samplesheet 
        samplesheet_path = args.output_file
        with open(samplesheet_path, "w") as ss_fp:
            create_csv([sample_data], args.seq_header, args.fasta_header, ss_fp)
    
    if mode == MODE_STRING_JSON:
        # Generate metadata for AA string
        aa_sample_name = sample_name(args.aa_string, seq_chars=args.seq_chars)
        aa_sample_file_name = file_name(aa_sample_name, prefix=args.aa_prefix, suffix=args.aa_suffix, extension=args.output_extension)
        aa_path = args.fasta_dir + "/" + aa_sample_file_name 

        # Create the fasta file
        sample_data = Sample(aa_sample_name, aa_path, args.aa_string)
        make_fasta(sample_data)

        if args.output_file == "samplesheet.csv":
            args.output_file = args.output_file.replace(".csv", ".json")
        samplesheet_path = args.output_file
        
        with open(samplesheet_path, "w") as ss_fp:
            create_json([sample_data], ss_fp)

    if mode == MODE_DIR_CSV:
        logger.debug(f"Checking {args.dir} for fasta files")
        file_list = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f))]         
        logger.debug(f"Fasta files: {file_list}")
        file_list = [i for i in file_list if re.search(args.fasta_regex, i)]
        logger.debug(f"File list aginst regex: {file_list}")
        sample_data = []

        for file_name in file_list:
            fasta_data = read_fasta(file_name, single_line=(not args.monomer))
            sample_data.extend(fasta_data)
            logger.debug(f"Added sample {file_name}, {fasta_data}")
        
        samplesheet_path = args.output_file
        logger.debug(f"Sample data array length: {len(sample_data)}")
        with open(samplesheet_path, "w") as ss_fp:
            create_csv(sample_data, args.seq_header, args.fasta_header, ss_fp)

    if mode == MODE_DIR_JSON:
        file_list = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f)) and re.search(args.fasta_regex, f)]         
        sample_data = []

        for file_name in file_list:
            with open(file_name, "r") as file_fp:
                sample_data.extend(read_fasta(file_fp, read_data=True, single_line=False))
        
        samplesheet_path = args.output_file

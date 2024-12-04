import argparse, tempfile, logging, os
from samplesheetutils.utils.fasta import *
from samplesheetutils.utils.input import *

logger = logging.getLogger(__name__)
logging.basicConfig()

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()
    # https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except

def sample_name():
    parser = argparse.ArgumentParser(
        prog="Read sample name(s) from FASTA",
        description="Utility to read the sample name(s) from a FASTA file and print them to stdout",
        epilog="Written by Nathan Glades <n.glades@unsw.edu.au>"
    )
    
    parser.add_argument('-i', '--index', help='Index of the sample you wish to output.\nIf unset, all sample names will be output. Acceptable inputs are an integer, -1 for the last sample, or a range (a:b)', default=None, dest='index')
    parser.add_argument('--debug', help='Enables debug output', default=False, action='store_true', dest='debug')
    parser.add_argument('--sanitize', '--sanitise', help='Enables input sanititation on sample names (usefull for passing to a bash command)', default=False, action='store_true', dest='sani')
    parser.add_argument('-d', '--delim', help='Delimiter between each sample name', default='\n', dest='delim')
    parser.add_argument('fasta', nargs='*')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.debug(f'Input file(s): {args.fasta}')

    samples = []
    for sample in args.fasta:
        with open(sample, "r") as sample_fp:
            samples.extend(read_fasta(sample_fp, single_line=False))

    if len(samples) == 0:
        print()
        exit(0)

    if args.index:
        if check_int(args.index):
            try:
                samples = [samples[int(args.index)]]
            except IndexError:
                logging.error(f'Index {args.index} out of range (range is 0-{str(len(samples))})')
                exit(1)
        elif check_int(args.index.replace(':', '')):
            # Janky way of checking if the user has input a range
            index_ints = [int(i) for i in args.index.split(':')]
            try:
                if len(index_ints) == 1:
                    samples = samples[index_ints[0]:]
                else:
                    samples = samples[index_ints[0]:index_ints[1]]
            except IndexError:
                logging.error(f'Index {args.index} out of range (range is 0-{str(len(samples))})')
                exit(1)
        else:
            logging.error(f'Invalid index input: {args.index}')
            exit(1)
    
    if args.sani:
        print(args.delim.join([sanitize_input(i.name) for i in samples]))
    else:
        print(args.delim.join([i.name for i in samples]))

# samplesheet-utils
`samplesheet-utils` (or `samplesheetutils`) is a collection of scripts and utilities for working with samplesheets and FASTA files at the command line. It is primarily designed for use within pipelines.

## Installation
### git
```bash
git clone https://github.com/Australian-Structural-Biology-Computing/create-samplesheet
cd create-samplesheet
pip3 install .
```

## Commands
### sample-name
This command is used to read the sample name(s) from a FASTA file. This is useful for dynamically creating directories based on the actual sample name.
```bash
sample-name [ARGS] [FASTA(s)]
```
- `-i --index`: Index of the sample you wish to read the name from. This can be an integer, -1 for the last sample, or a range `(1:5)`
- `--sanitize --sanitise`: Replaces any problematic characters in the sample name(s) with an underscore
- `-d --delim`: Change the delimiter between each sample name. By default this is a new-line character

### create-samplesheet
This command is used to create a samplesheet from different inputs, including string, and directories containing FASTA files
```bash
create-samplesheet [ARGS]
```
- `-a --aa-string`: Input a single amino acid sequence
- `-d --directory`: Input a directory containing FASTA files
- `-o --output-file`: Samplesheet filename. Default is `samplesheet.[ext]` [ext] depends on mode
- `-j --json`: Ouptut JSON formatted samplesheet
- `-y --yaml`: Output YAML formatted samplesheet

### TODO
- [ ] Finish documentation

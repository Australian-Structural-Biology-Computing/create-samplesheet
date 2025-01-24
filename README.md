# samplesheet-utils
![Testing](https://github.com/Australian-Structural-Biology-Computing/create-samplesheet/actions/workflows/python-app.yml/badge.svg)

`samplesheet-utils` (or `samplesheetutils`) is a collection of scripts and utilities for working with samplesheets and FASTA files at the command line. It is primarily designed for use within pipelines.

## Installation
### pip
```bash
pip3 install samplesheetutils
```
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
- `-m --msa-dir`: Directory to search for corresponding MSA files in (Only accessible in yaml output)

#### `--msa-dir`
When using the YAML output mode (`-y`, `--yaml`), you can provide a path to a directory containg sample's pre-computed multiple sequence alignment files (`.a3m` files). In order for these files to automatically be associated with it's corresponding sample, the filenames must follow the following format:

```
[SAMPLE NAME].a3m
```

**Example Usage:**
```bash
create-samplesheet --directory /home/nathan/experiment/fastas --msa-dir /home/nathan/experiment/fastas/msas --yaml
```

**Directory Structure**
```
/home/nathan/experiment/fastas
├── A1.fasta
├── A2.fasta
└── msas
    ├── A1.m3a
    └── A2.m3a
```

### TODO
- [ ] Finish documentation

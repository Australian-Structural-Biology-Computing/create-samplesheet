class Sample:
    def __init__(self, name, path, data, msa = None):
        self.name = name
        self.path = path
        self.data = data
        self.msa = msa

def sample_name(aa_seq, seq_chars=6):
    trunc_aa_seq = aa_seq[:min(seq_chars, len(aa_seq))]
    return trunc_aa_seq

def file_name(sample_id, prefix='manual_entry', suffix='af2', delim='-', extension='fasta'):
    return ''.join([prefix, delim, sample_id, delim, suffix, '.', extension])


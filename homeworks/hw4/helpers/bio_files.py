import os


def read_fasta(fasta_file: str):
    with open(fasta_file, 'r') as input_file:
        seq: list = []
        id: str = None
        while True:
            line = input_file.readline().strip()
            if line == (''):
                break
            if line.startswith('>'):
                if id != None:
                    yield id, ''.join(seq)
                    id = line
                    seq = []
                else:
                    id = line
            else:
                seq.append(line)
        if id != None:
            yield id, ''.join(seq) 


def read_blast_results(input_file: str):
    with open(input_file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if "Sequences producing significant alignments:" in line:
                    filler, filler = f.readline(), f.readline()
                    out_line: str = f.readline().split('  ')[0]
                    yield out_line
                    continue
                continue

        
            

# импорты

import os
from helpers.fastq import (
    read_fastq,
    parse_gc_bounds,
    is_gc_pass,
    parse_length_bounds,
    is_length_pass,
    is_qualitative
    )


# filter_fastq
def filter_fastq(
    input_fastq, 
    output_fastq: str = 'filter_fastq_out.fastq', 
    gc_bounds: tuple = (0, 100), 
    length_bounds: tuple = (0, 2**32), 
    quality_threshold: int = 0): 
    """
    returns strings with specified params
    Filtered reads are saved to the `filtered` folder

    Arguments:
    input_fastq — path to the input FASTQ file
    output_fastq — name of the output file
    gc_bounds — GC content range (in percent) for filtering (default is (0, 100). Single number is treated as the upper bound.
    length_bounds — length range for filtering; works similarly to `gc_bounds`, but the default is (0, 2**32)
    quality_threshold — threshold value for average read quality used for filtering; default is 0 (Phred33 scale)

    """
    filtered_dir = os.path.join(os.getcwd(), 'filtered')
    os.makedirs(filtered_dir, exist_ok= True)

    gc_from, gc_to = parse_gc_bounds(gc_bounds)
    len_from, len_to = parse_length_bounds(length_bounds)

    file = open(f'filtered\\{output_fastq}', 'w')
    file.close()

    for id, sequence, separator, quality_line in read_fastq(input_fastq):
        if not is_gc_pass(sequence, gc_from, gc_to):
            continue
        if not is_length_pass(sequence, len_from, len_to):
            continue
        if not is_qualitative(quality_line, quality_threshold):
            continue
        with open(f'filtered\\{output_fastq}', 'a') as out:
            out.write(id + '\n')
            out.write(sequence + '\n')
            out.write(separator + '\n')
            out.write(quality_line + '\n')
# B1
def convert_multiline_fasta_to_oneline(input_fasta, output_fasta = 'onelined.fasta'):
    """
    input_fasta - path to input file
    output_fasta - name of the output file

    reads the input FASTA and saves it to a new FASTA file where 
    the sequence fits on a single line.
    """
    from helpers.bio_files import read_fasta
    for id, sequence in read_fasta(input_fasta):
        with open(f'helpers\\filtered\\{output_fasta}', 'a') as out:
            out.write(id + '\n')
            out.write(sequence + '\n')

#B2
def parse_blast_result(input_file, output_file='parse_blast_result_output.txt'):
    """
    input_fasta - path to input file
    output_fasta - name of the output file

    For each query saves the first line from the "Description" column, sorted alphabetically.
    """
    from helpers.bio_files import read_blast_results
    with open(output_file, 'w') as out:
        buffer : list[str] = []
        for line in read_blast_results(input_file):
            buffer.append(f'{line[0:64]}\n')
        buffer.sort()    
        for line in buffer:
            out.write(line)
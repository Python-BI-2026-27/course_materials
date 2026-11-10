import os

# fastq reading
def read_fastq(path_to_fastq) -> generator:
    with open(path_to_fastq, 'r') as input_file:
        while True:
            id: str = input_file.readline().strip()
            if id == '':
                break 
            sequence: str = input_file.readline().strip()
            separator: str = input_file.readline().strip()
            quality_line: str = input_file.readline().strip()
            yield id, sequence, separator, quality_line


# Parsing and gc_num check
def parse_gc_bounds(gc_bounds: tuple or int):
    gc_from: str = 0
    gc_to = 100
    if gc_bounds is None:
        return start, end
    if isinstance(gc_bounds, (int, float)):
        gc_to = gc_bounds
        return start, end
    if isinstance(gc_bounds, (list, tuple)):
        gc_from = gc_bounds[0]
        gc_to = gc_bounds[1]
        return gc_from, gc_to
def is_gc_pass(sequence: str,
 gc_from: int, gc_to: int):
    gc_num = sequence.count('G') + sequence.count('C')
    return gc_from < gc_num < gc_to


# length parsing and check
def parse_length_bounds(length_bounds: tuple or int):
    len_from: int = 0
    len_to: int = 2**32
    if length_bounds is None:
        return len_from, len_to
    if isinstance(length_bounds, (int, float)):
        len_to = length_bounds
        return len_from, len_to
    if isinstance(length_bounds, (list, tuple)):
        len_from = length_bounds[0]
        len_to = length_bounds[1]
        return len_from, len_to
def is_length_pass(sequence: str, len_from: int, len_to: int) -> bool:
    return len_from < len(sequence) < len_to


# quality check
def is_qualitative(quality_line: str, threshold: int) -> bool:
    quality_decoded = [ord(i) - 33 for i in quality_line]
    mean_quality = sum(quality_decoded) / len(quality_decoded)
    return mean_quality >= threshold


# def filter_fastq(
#     input_fastq: str, 
#     output_fastq: str = 'filter_fastq_out.fastq', 
#     gc_bounds: tuple = (0, 100), 
#     length_bounds: tuple = (0, 2**32), 
#     quality_threshold: int = 0):
    
#     os.makedirs(filtered_dir, exist_ok= True)

#     gc_from, gc_to = parse_gc_bounds(gc_bounds)
#     len_from, len_to = parse_length_bounds(length_bounds)

#     file = open(f'filtered\\{output_fastq}', 'w')
#     file.close()

#     for id, sequence, separator, quality_line in read_fastq(input_fastq):
#         if not is_gc_pass(sequence, gc_from, gc_to):
#             continue
#         if not is_length_pass(sequence, len_from, len_to):
#             continue
#         if not is_qualitative(quality_line, quality_threshold):
#             continue
#         with open(f'filtered\\{output_fastq}', 'a') as out:
#             out.write(id + '\n')
#             out.write(sequence + '\n')
#             out.write(separator + '\n')
#             out.write(quality_line + '\n')
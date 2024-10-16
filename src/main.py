import time

import numpy as np
from printer import print_table
from solver import solve
from tabler import read_table

files = [
    # "input_files/s1.txt",
    # "input_files/s2.txt",
    # "input_files/s3.txt",
    "input_files/s4.txt",
    "input_files/s5.txt",
    "input_files/s6.txt",
    "input_files/s7.txt",
    "input_files/s8.txt",
    "input_files/s9.txt",
    "input_files/s10.txt",
    "input_files/s11.txt",
    "input_files/s12.txt",
]

for file in files:
    print(f"\nSolving {file}...")
    table = read_table(file)
    print_table(table)

    start = time.time()
    solution = solve(table.copy(), tqdm_disable=False)
    end = time.time()
    print(f"Solution with {np.max(solution)} squares in {(end - start):.4f}s:")
    print_table(solution)


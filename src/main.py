

from tabler import read_table
from printer import print_table
from solver import random_solve
import time

table = read_table("input_files/s1.txt")
print_table(table)

start = time.time() * 1000
solution = random_solve(table)
end = time.time() * 1000
print(f"Time: {end - start:.2}ms")

print("Solution:", solution)
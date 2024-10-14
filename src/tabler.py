from typing import List

import numpy as np


def read_table(input_path: str) -> List[List[str]]:
    with open(input_path, "r") as f:
        lines = [line for line in f]
    x = int(lines[0])
    y = int(lines[1])
    table = np.array([0 if char == '1' else -1 for char in lines[2]])
    table = table.reshape(x, y)
    return table

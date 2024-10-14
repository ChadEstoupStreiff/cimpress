from typing import List

import numpy as np


def border_table(table, x, y):
    return [
        1 if x == 0 or table[x - 1][y] != -1 else 0,
        1 if x == table.shape[0] - 1 or table[x + 1][y] != -1 else 0,
        1 if y == 0 or table[x][y - 1] != -1 else 0,
        1 if y == table.shape[1] - 1 or table[x][y + 1] != -1 else 0,
    ]  # TOP, BOTTOM, LEFT, RIGHT


def get_corners(table):
    coords = np.argwhere(table == -1)
    corners = []

    for x, y in coords:
        borders = border_table(table, x, y)
        if np.sum(borders) >= 2:
            corners.append((x, y))

    return corners

def read_table(input_path: str) -> List[List[str]]:
    with open(input_path, "r") as f:
        lines = [line for line in f]
    x = int(lines[0])
    y = int(lines[1])
    table = np.array([0 if char == "1" else -1 for char in lines[2]])
    table = table.reshape(x, y)
    return table

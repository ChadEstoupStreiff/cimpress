
import numpy as np
from tabler import border_table, get_corners
from tqdm import tqdm
from printer import print_table


def is_empty(table):
    return np.all(table == -1)


def is_complete(table):
    return -1 not in table


def place_square(table, x, y, depth_index):
    border = border_table(table, x, y)
    x_dir = 1 if border[0] == 1 else -1
    y_dir = 1 if border[2] == 1 else -1
    size = 0

    x_b = x + x_dir * size
    y_b = y + y_dir * size

    while True:
        x_b = x + x_dir * size
        y_b = y + y_dir * size
        if (
            x_b < 0
            or x_b > table.shape[0]
            or y_b < 0
            or y_b > table.shape[1]
            or not is_empty(table[min(x, x_b) : max(x, x_b), min(y, y_b) : max(y, y_b)])
        ):
            break
        size += 1

    size -= 1
    if size > 0:
        x_b = x + x_dir * size
        y_b = y + y_dir * size
        table[min(x, x_b) : max(x, x_b), min(y, y_b) : max(y, y_b)] = depth_index
    return table



def random_solve(table, square_index=1, tqdm_disable=True):
    # Check if complete
    if is_complete(table):
        return table

    # Remove small ones
    corners = get_corners(table)
    for x, y in corners:
        border = border_table(table, x, y)
        if (
            sum(border) > 2
            or (border[0] == 1 and border[1] == 1)
            or (border[2] == 1 and border[3] == 1)
        ):
            table[x, y] = square_index
            square_index += 1

    # Calculate bigger square possible on corners
    if is_complete(table):
        return table
    corners = get_corners(table)

    solutions = []
    for x, y in tqdm(corners, disable=tqdm_disable):
        new_table = table.copy()

        new_table = place_square(new_table, x, y, square_index)

        sol = random_solve(new_table, square_index=square_index + 1)
        solutions.append(sol)

    # Find best solution
    min_number = np.inf
    best_sol = None
    for sol in solutions:
        max_sol_value = np.max(sol)
        if max_sol_value < min_number:
            min_number = max_sol_value
            best_sol = sol
    return best_sol

import numpy as np
from printer import print_table
from tabler import border_table, get_corners


def is_empty(table):
    return np.all(table == -1)


def is_complete(table):
    return -1 not in table


def random_solve(table, depth_index=1, verbose=True):
    old_table = table.copy()
    if verbose:
        print("\n\nDepth index:", depth_index)
    corners = get_corners(table)
    x, y = corners[0]
    border = border_table(table, x, y)

    if (
        sum(border) > 2
        or (border[0] == 1 and border[1] == 1)
        or (border[2] == 1 and border[3] == 1)
    ):
        table[x, y] = depth_index
        x_b, y_b = x+1, y+1
    else:
        x_dir = 1 if border[0] == 1 else -1
        y_dir = 1 if border[2] == 1 else -1
        size = 0

        x_b = x + x_dir * size
        y_b = y + y_dir * size
        while (
            x_b >= 0
            and x_b < table.shape[0]
            and y_b >= 0
            and y_b < table.shape[1]
            and is_empty(table[x:x_b, y:y_b])
        ):
            size += 1
            x_b = x + x_dir * size
            y_b = y + y_dir * size
        size -= 1
        x_b = x + x_dir * size
        y_b = y + y_dir * size
        table[x:x_b, y:y_b] = depth_index
        print(size)

    if np.array_equal(old_table, table):
        print("No changes")
        exit()

    if verbose:
        print_table(table, highlights=[x, y, x_b, y_b])
    if is_complete(table):
        return table
    return random_solve(table, depth_index=depth_index + 1, verbose=verbose)

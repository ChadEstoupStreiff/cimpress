import numpy as np
from tabler import border_table, get_corners, get_isolated
from tqdm import tqdm


def is_empty(table):
    return np.all(table == -1)


def is_complete(table):
    return -1 not in table


def place_square(table, x_a, y_a, depth_index):
    border = border_table(table, x_a, y_a)
    x_dir = 1 if border[0] == 1 else -1
    y_dir = 1 if border[2] == 1 else -1
    size = 1

    while True:
        x_b = x_a + x_dir * size
        y_b = y_a + y_dir * size
        if (
            x_b < 0
            or x_b >= table.shape[0]
            or y_b < 0
            or y_b >= table.shape[1]
            or not is_empty(
                table[
                    min(x_a, x_b) : max(x_a, x_b) + 1, min(y_a, y_b) : max(y_a, y_b) + 1
                ]
            )
        ):
            break
        size += 1

    size -= 1
    x_b = x_a + x_dir * size
    y_b = y_a + y_dir * size
    table[min(x_a, x_b) : max(x_a, x_b) + 1, min(y_a, y_b) : max(y_a, y_b) + 1] = (
        depth_index
    )
    return table


def fill_isolated(table, square_index, max_authorized_index):
    isolated = get_isolated(table)
    while len(isolated) > 0:
        for x, y in isolated:
            table[x, y] = square_index
            square_index += 1
            if square_index > max_authorized_index:
                return None, square_index
        isolated = get_isolated(table)
    return table, square_index


def does_sol_exists(table, solutions):
    for sol in solutions:
        if np.array_equal(sol, table):
            return True
    return False


def solve(table, square_index=1, max_authorized_index=np.inf, tqdm_disable=True):
    # Check if complete
    if is_complete(table):
        return table

    if square_index > max_authorized_index:
        return None

    # Remove small ones
    table, square_index = fill_isolated(
        table, square_index, max_authorized_index=max_authorized_index
    )

    # Calculate bigger square possible on corners
    if table is None or is_complete(table):
        return table
    corners = get_corners(table)

    solutions = []
    for x, y in tqdm(corners, disable=tqdm_disable):
        new_table = table.copy()

        new_table = place_square(new_table, x, y, square_index)
        if is_complete(new_table):
            return new_table

        if not does_sol_exists(new_table, solutions):
            sol = solve(
                new_table,
                square_index=square_index + 1,
                max_authorized_index=max_authorized_index,
            )
            if sol is not None:
                if np.max(sol) < max_authorized_index:
                    max_authorized_index = np.max(sol)
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

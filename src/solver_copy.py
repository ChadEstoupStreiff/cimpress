import numpy as np
from tabler import border_table, get_corners, get_isolated
from tqdm import tqdm


def is_empty(table):
    return np.all(table == -1)

def is_complete(table):
    return -1 not in table

def does_sol_exists(table, solutions):
    for sol in solutions:
        if np.array_equal(sol, table):
            return True
    return False


def fill_isolated(table, square_index, max_authorized_index):
    isolated = get_isolated(table)
    while len(isolated) > 0:
        for x, y in isolated:
            table[x, y] = square_index
            square_index += 1
            if square_index > max_authorized_index:
                return None
        isolated = get_isolated(table)
    return square_index


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

# Return the best solution for the table, return None if out of limits
# Do a copy instead of revert, a bit faster (10%)
def solve(table, square_index=1, tqdm_disable=True, max_authorized_index=np.inf):

    # Check if complete
    if is_complete(table):
        return table.copy()
    
    # Fill isolated spaces
    square_index = fill_isolated(table, square_index, max_authorized_index)
    if square_index is None:
        # If filling isolated cells goes beyond the limit, return None
        return None
    
    # Check if completed after filling isolated spaces
    if is_complete(table):
        return table.copy()
    
    corners = get_corners(table)

    best_sol = None
    best_sol_index = np.inf

    for x_a, y_a in tqdm(corners, disable=tqdm_disable):
        # Place the square and modify the table

        new_table = table.copy()
        place_square(new_table, x_a, y_a, square_index)

        # Recursive call to solve_copy, not solve
        sol = solve(new_table, square_index + 1, max_authorized_index=max_authorized_index)
        if sol is not None:
            sol_index = np.max(sol)
            # If the solution is better, update the best solution
            if sol_index < best_sol_index:
                best_sol = sol
                best_sol_index = sol_index
                max_authorized_index = best_sol_index

    return best_sol
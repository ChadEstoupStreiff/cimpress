from tabler import get_corners
from termcolor import colored


def print_table(table, print_corners=True, highlights=None):
    if highlights is not None:
        table = table.copy()
        table[highlights[0] : highlights[2], highlights[1] : highlights[3]] = -2
        print("Highlights:", highlights)
    else:
        print("No highlights")
    corners = []
    if print_corners:
        corners = get_corners(table)

    def get_color_for_cell(x, y):
        if table[x][y] == -2:
            return "green"
        if (x, y) in corners:
            return "red"

        if table[x][y] == 0:
            return "light_grey"
        return "dark_grey"

    for y in range(table.shape[0]):
        for x in range(table.shape[1]):
            print(
                colored("  ■", get_color_for_cell(x, y))
                if table[x][y] < 1
                else f"{table[x][y]:3}",
                end="",
            )
        print()

from termcolor import colored


def print_table(table):
    for x in range(10):
        for y in range(10):
            print(colored("■ ", "light_grey" if table[x][y] == 0 else "dark_grey"), end="")
        print()

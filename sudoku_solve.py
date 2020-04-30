"""
Author: Akshat Naik
Sudoku Solver
July 2019
"""

import os
from time import sleep
try:
    from colorama import Fore, Back, Style
except ImportError:
    pass


def cross(A, B):
    """Cartesian product of strings A and B."""
    return [a+b for a in A for b in B]


rows = "ABCDEFGHI"
cols = "123456789"
cells = cross(rows, cols)  # Cartesian product of cell names
unitlist = ([cells[9*i:9*(i+1)] for i in range(9)]
          + [cells[i::9] for i in range(9)] 
          + [cells[i:i+3] + cells[i+9:i+12] + cells[i+18:i+21] for i in [0,3,6,27,30,33,54,57,60]])
# List of units which have cells with common Alldiff Constraint
units = {cell:[] for cell in cells} 
# Each cell: list of units to which it belongs
for unit in unitlist:
    for cell in unit:
        units[cell].append(unit)
peers = {cell: (set(unit[0] + unit[1] + unit[2]) - set([cell])) for cell, unit in units.items()}
# Each cell: peers who share Alldiff Constraint

# Assuming all problems are assignable with the correct format listed below
def grid_values(grid):
    """Assigns all cells to values/possible values in a dict.
    
    grid: string of values filled in the given Sudoku problem.    
    """
    values = {cell:"123456789" if val == "0" else val for cell, val in zip(cells, grid)}
    return values


def elimination(squares, values, demo=False):
    """Eliminates values based on Alldiff constraint using confirmed values.

    square: set of cells required to check if there is only one value.
    values: dict of cell-value pairs.
    """
    # Returns True if changed, False if not changed, "Failure" if there is no assignment possible
    change = False
    while squares:
        square = squares.pop()
        val = values[square]
        if len(val) == 1:
            for cell in peers[square]:
                if val in values[cell]:
                    change = True
                    values[cell] = values[cell].replace(val, "")
                    squares.add(cell)
                    if demo:
                        clear_terminal()
                        display(values)
                        sleep(0.001)
        elif len(val) == 0:
            return "Failure"
    return change


def assign(unit_list, values, set_cells, demo=False):
    """Assigns a value to a cell if no other peer in its unit can possibly have
    that value.

    unit_list: list of units where each cell is a peer of each other having
        Alldiff contraint.
    set_cells: set of cells for elimination to check after first iteration.
    values: dict of cell-value pairs.
    """
    # Returns True if changed, False if not changed
    change = False
    for unit in unit_list:
        numbers = [[],[],[],[],[],[],[],[],[]]
        for cell in unit:
            for val in values[cell]:
                numbers[int(val)-1].append(cell)
        for ind, a in enumerate(numbers):
            if len(a) == 1:
                values[a[0]] = str(ind + 1)
                set_cells.add(a[0])
                change = True
                if demo:
                    clear_terminal()
                    display(values)
                    sleep(0.001)
    return change

def display(values):
    """Display/Prints values as 2-D Grid."""
    width = 1+max(len(values[cell]) for cell in cells)
    line = '+'.join(['-'*(width*3)]*3)
    try:
        print(Fore.BLACK+ Back.YELLOW)
        for r in rows:
            print("".join(values[r+c].center(width) + ("|" if c in "36" else "") for c in cols))
            if r in "CF":
                print(line)
        print(Style.RESET_ALL)
    except NameError:
        for r in rows:
            print("".join(values[r+c].center(width) + ("|" if c in "36" else "") for c in cols))
            if r in "CF":
                print(line)

def writetofile(values):
    """Writes (appends to be more accurate) values as 2-D Grid in 
    solutions.txt.
    """
    with open("solutions.txt", "a") as f:
        width = 1+max(len(values[cell]) for cell in cells)
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            text = ("".join(values[r+c].center(width) + ("|" if c in "36" else "") for c in cols))
            f.write(text + "\n")
            if r in "CF":
                f.write(line + "\n")
        f.write("\n")

def least_values(squares, values):
    """Finds out the or one of the cells with least number of possible values != 1."""
    length, min_square = min((len(values[square]), square) for square in squares if len(values[square]) > 1)
    return length, min_square

def solve_simple(squares, values, demo=False):
    """Employs simple mechanical rules to reduce/solve a Sudoku puzzle."""
    boolean = True
    set_cells = set(squares)
    while boolean:
        bool1 = elimination(set_cells, values, demo)
        if bool1 == "Failure":
            return False
        bool2 = assign(unitlist, values, set_cells, demo)
        boolean = bool1 and bool2
    return True

def search(squares, values, demo=False):
    """Writes the solution to the file solution.txt if a solution exists.
    
    Returns: 
        True if solved, False if a contradiction is reached, implying problem
        has no solution.
    """
    if not solve_simple(squares, values, demo):
        return False
    elif all(len(values[s])==1 for s in squares):
        writetofile(values)
        return True
    _, min_square = least_values(squares, values)
    for val in values[min_square]:
        values_dict = values.copy()
        values_dict[min_square] = val
        if search(squares, values_dict, demo):
            return True
    return False


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

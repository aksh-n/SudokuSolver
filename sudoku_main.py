import sudoku_solve as sdoku
from time import time

def demo():
    print("Welcome to the demonstration.")
    print("This Sudoku solver's heart is the use of constriant propagation, which eliminates conflicting values.")
    print("Each empty cell in a Sudoku grid is represented by all values (1 to 9) initially.")
    print("As values keep getting eliminated, only one value for each cell remains and, a solution emerges.")
    print("In addition to constraint propagation, I have implemented depth-first search to ensure completeness.")
    problem = sdoku.grid_values("000000010400000000020000000000050407008000300001090000300400200050100000000806000")
    print("I have selected a sample problem.")
    print("Note that the solving has been intentionally slowed by a factor of ~3500 for demonstration purposes.")
    print("Now sit back and enjoy!")
    print("\n\n")
    print("SAMPLE SUDOKU PUZZLE: \n")
    sdoku.display(problem)
    input("Press Enter to start solving!")
    sdoku.search(sdoku.cells, problem, True)

def solve_file(puzzle_file):
    with open(puzzle_file, "r") as f:
        data = f.readlines()
    puzzle_times = []
    for line in data:
        start_mini = time()
        sdoku.search(sdoku.cells, sdoku.grid_values(line))
        end_mini = time()
        puzzle_times += [end_mini - start_mini]
    avg_time = round(sum(puzzle_times)/len(puzzle_times), 5)
    max_time = round(max(puzzle_times), 5)
    avg_Hz = int(1/avg_time)
    print("Average time taken for {0} ({1} puzzle) is {3} secs ({2} Hz) with maximum time taken as {4} secs".format(puzzle_file, len(puzzle_times), avg_Hz, avg_time, max_time))



def menu():
    with open("solutions.txt", "w") as f:
        pass
    print("\n")
    print("Welcome to my Sudoku Solver.")
    print("This Sudoku Solver is capable of solving all Sudoku problems possessing a unique solution with an average of less than 0.01 seconds.")
    while True:
        print("All solutions are written in solution.txt.")
        print("Data is cleared each time a new file is chosen to be solved.\n")
        print("MENU: ")
        print("1) Demonstration: Please choose if this is your first time.")
        print("2) Solve easy puzzles.")
        print("3) Solve medium puzzles.")
        print("4) Solve hardest puzzles.")
        print("5) Solve A LOT of hard puzzles (~50 thousand).")
        print("0) To quit this program.")
        option = input("Enter your option: ")
        print("\n")
        if option in ["1", "2", "3", "4", "5"]:
            with open("solutions.txt", "w") as f:
                pass
        if option == "1":
            demo()
        elif option == "2":
            solve_file("sudoku_easy")
        elif option == "3":
            solve_file("sudoku_medium")
        elif option == "4":
            solve_file("sudoku_hard")
        elif option == "5":
            solve_file("sudoku_17")
        elif option == "0":
            break
        print("\n\n")

menu()

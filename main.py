import numpy as np
from sudoku import Sudoku

from puzzles import puzzles
from SGP import SGP
from reducers.sudoku_to_sgp import sudoku_to_SGP, is_solution_tiled, get_solution_tile
from reducers.latin_to_SGP import latin_to_SGP

from sgp_solver import Solve_SGP
from visualizer.visualizer import visualize_SGP

latin_square_array = np.array([
    [1, None, None],
    [2, None, None],
    [None, None, None]
])

#latin_square_array = np.full((3,3), None)


puzzle = latin_to_SGP(latin_square_array)


solutions = Solve_SGP(puzzle, get_all=True, log_progress=False)

for solution_df in solutions:
    solution = solution_df.sort_values(by=["row", "col"])
    solution = solution.values.reshape((solution_df["row"].max() + 1, -1, 3))

    solution = solution[:, :, 2] + 1
    print(solution)
    print()
print(len(solutions), "solutions found.")
#visualize_SGP(puzzle)

"""
Sudoku:


width = 2
height = 2
sudoku_puzzle = Sudoku(width, height, seed=7).difficulty(0.5)
sudoku_puzzle.show()

print("Solved Sudoku:")
sudoku_solution = sudoku_puzzle.solve()
sudoku_solution.show()

print("-------------")



puzzle = sudoku_to_SGP(sudoku_puzzle)



solutions = Solve_SGP(puzzle, get_all=True, log_progress=True)

# Problems:
# Not every "solution" is tiled
# Not every "solution" is valid sudoku
# Sometimes no solutions are found when there should be at least 1 (width=3, height=2)
not_valid_sudoku = 0
not_tiled = 0
correct = 0

for solution_df in solutions:
    # Sort the df so the solution is read in reading order
    # Get only the color number
    # Convert from 0 indexing to 1 indexing

    solution = solution_df.sort_values(by=["row", "col"]).values.reshape((solution_df["row"].max() + 1, -1, 3))[:, :, 2] + 1
    sudoku_part = get_solution_tile(solution)
    temp_sudoku = Sudoku(width, height, board=sudoku_part.tolist())

    tiled = is_solution_tiled(solution)
    valid = temp_sudoku.validate()

    if not valid:
        not_valid_sudoku += 1

    if not tiled:
        not_tiled += 1

    if tiled and valid:
        correct += 1
        print("Correct Solution:")
        print(solution)
        print()
        print(sudoku_part)
        print("==================")
    else:
        print("Incorrect Solution:")
        print(solution)
        print("==================")


print("Total Solutions Found:", len(solutions))
print("'Solutions' that are not valid sudoku:", not_valid_sudoku)
print("'Solutions' that are not tiled:", not_tiled)
print("Correct Solutions Found:", correct)
"""
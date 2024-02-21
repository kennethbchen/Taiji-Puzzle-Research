from puzzles import puzzles
from SGP import SGP

from reducers.sudoku_to_sgp import sudoku_to_SGP
from sudoku import Sudoku

from sgp_solver import Solve_SGP

from visualizer.visualizer import visualize_SGP

sudoku_puzzle = Sudoku(3, 3).difficulty(0.5)
sudoku_puzzle.show()
print("Solved Sudoku:")
sudoku_solution = sudoku_puzzle.solve()
sudoku_solution.show()


puzzle = sudoku_to_SGP(sudoku_puzzle)

#visualize_SGP(puzzle)

solutions = Solve_SGP(puzzle, get_all=True, log_progress=False)

for solution_df in solutions:
    # Sort the df so the solution is read in reading order
    # Get only the color number
    # Convert from 0 indexing to 1 indexing
    solution = solution_df.sort_values(by=["row", "col"]).values.reshape((solution_df["row"].max() + 1, -1, 3))[:, :, 2] + 1
    print("Solved SGP:")
    print(solution)

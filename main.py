from puzzles import puzzles
from SGP import SGP

from reducers.sudoku_to_sgp import sudoku_to_SGP
from sudoku import Sudoku

from sgp_solver import Solve_SGP

from visualizer.visualizer import visualize_SGP

sudoku_puzzle = Sudoku(2,2).difficulty(0.5)
puzzle = sudoku_to_SGP(sudoku_puzzle)

#visualize_SGP(puzzle)

solutions = Solve_SGP(puzzle, get_all=False, log_progress=False)
solution = solutions[0]


for row in range(puzzle.board_shape()[0]):
    for col in range(puzzle.board_shape()[1]):
        print(solution.query("row=={r} and col=={c}".format(r=row, c=col))["color"].values[0], end=" ")
    print()

"""
# Solve and visualize puzzle
puzzle = SGP.from_dict(puzzles["taiji"])

solutions = Solve_SGP(puzzle)

# Convert numpy array to list of tuples
solution = list(map(tuple, solutions[0].values[:, 0:2]))

visualize_SGP(puzzle, symbol_data=solution)
"""
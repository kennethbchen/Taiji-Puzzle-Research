from puzzles import puzzles
from SGP import SGP

from reducers.sudoku_to_sgp import sudoku_to_SGP
from sudoku import Sudoku

from sgp_solver import Solve_SGP

from visualizer.visualizer import visualize_SGP

sudoku_puzzle = Sudoku(3).difficulty(0.5)
puzzle = sudoku_to_SGP(sudoku_puzzle)
visualize_SGP(puzzle)

"""
# Solve and visualize puzzle
puzzle = SGP.from_dict(puzzles["taiji"])

solutions = Solve_SGP(puzzle)

# Convert numpy array to list of tuples
solution = list(map(tuple, solutions[0].values[:, 0:2]))

visualize_SGP(puzzle, symbol_data=solution)
"""
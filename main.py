from puzzles import puzzles
from SGP import SGP

from sgp_solver import Solve_SGP

from visualizer.visualizer import visualize_SGP

# Solve and visualize puzzle
puzzle = SGP.from_dict(puzzles["8queens"])

solutions = Solve_SGP(puzzle)

# Convert numpy array to list of tuples
solution = list(map(tuple, solutions[0].values[:, 0:2]))

visualize_SGP(puzzle, symbol_data=solution)

import numpy as np

from reducers.latin_to_SGP import latin_to_SGP, untile_sgp_solution_array

from sgp_solver import Solve_SGP
from visualizer.visualizer import visualize_SGP

"""
latin_square_array = np.array([
    [1, None, None],
    [None, None, None],
    [None, 1, None]
])
"""

latin_square_array = np.full((3, 3), None)

puzzle = latin_to_SGP(latin_square_array)

solutions = Solve_SGP(puzzle, get_all=True, log_progress=False)

for solution_df in solutions:
    solution = solution_df.sort_values(by=["row", "col"])
    solution = solution.values.reshape((solution_df["row"].max() + 1, -1, 3))

    solution = solution[:, :, 2] + 1
    print(untile_sgp_solution_array(solution))
    print()
print(len(solutions), "solutions found.")

from puzzles import puzzles
from SGP import SGP

from reducers.sudoku_to_sgp import sudoku_to_SGP
from sudoku import Sudoku

from sgp_solver import Solve_SGP

from visualizer.visualizer import visualize_SGP

sudoku_puzzle = Sudoku(2, 2).difficulty(0.5)
sudoku_puzzle.show()
print("Solved Sudoku:")
sudoku_solution = sudoku_puzzle.solve()
sudoku_solution.show()


puzzle = sudoku_to_SGP(sudoku_puzzle)

#visualize_SGP(puzzle)

solutions = Solve_SGP(puzzle, get_all=False, log_progress=False)
solution = solutions[0]

print("Solved SGP:")
for row in range(puzzle.board_shape()[0]):
    for col in range(puzzle.board_shape()[1]):
        print(solution.query("row=={r} and col=={c}".format(r=row, c=col))["color"].values[0] + 1, end=" ")
    print()

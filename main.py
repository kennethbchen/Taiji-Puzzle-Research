from puzzles import puzzles
from SGP import SGP

from sgp_solver import Solve_SGP

puzzle = SGP.from_dict(puzzles["taiji"])

solutions = Solve_SGP(puzzle)

print(solutions)
print("{n} Solutions Found".format(n=len(solutions)))

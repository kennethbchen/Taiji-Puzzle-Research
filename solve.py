from ortools.sat.python import cp_model
import pandas as pd

model = cp_model.CpModel()

# 3x3 grid of cells
cells = []
for i in range(3):
    row = []
    for j in range(3):
        row.append(model.NewBoolVar(f'cell_{i}_{j}'))
    cells.append(row)

# define two regions for first board
region1 = [cells[0][0], cells[0][1], cells[0][2]]
region2 = [cells[1][0], cells[1][1], cells[1][2], cells[2][0], cells[2][1], cells[2][2]]

regions = [region1, region2]

for region in regions:
    left_or_var = model.NewBoolVar('')
    right_or_var = model.NewBoolVar('')
    model.AddBoolXOr([left_or_var, right_or_var])
    model.Add(sum(region) == 2).OnlyEnforceIf(left_or_var)
    model.Add(sum(region) == 0).OnlyEnforceIf(right_or_var)

model.Add(sum([c for row in cells for c in row]) == 4)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    for i in range(3):
        for j in range(3):
            if solver.Value(cells[i][j]):
                print('O', end='')
            else:
                print('.', end='')
        print()
else:
    print('No solution found')

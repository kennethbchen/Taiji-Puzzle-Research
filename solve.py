from ortools.sat.python import cp_model

model = cp_model.CpModel()

symbols = 8
region_capacity = 2

# All boards should be the same size
# Each cell in a board has an integer which represents its region id
# cells that have the same region id are considered in the same region
boards = [
    [
        [1, 1, 1, 1, 1, 4],
        [2, 2, 2, 2, 1, 4],
        [2, 3, 3, 2, 1, 4],
        [2, 3, 4, 1, 1, 4],
        [2, 3, 4, 4, 4, 4],
        [2, 3, 3, 3, 3, 3],
    ],
    [
        [1, 1, 1, 1, 1, 2],
        [3, 3, 3, 3, 1, 2],
        [3, 3, 3, 4, 2, 2],
        [5, 3, 4, 4, 4, 2],
        [5, 3, 3, 3, 3, 6],
        [5, 5, 3, 3, 7, 8],
    ],
    [
        [1, 1, 1, 2, 2, 7],
        [1, 2, 2, 2, 8, 9],
        [1, 2, 3, 3, 10, 11],
        [1, 1, 4, 4, 1, 6],
        [5, 1, 4, 1, 1, 6],
        [5, 1, 1, 1, 6, 6],
    ]
]

rows, cols = len(boards[0]), len(boards[0][0])

# Create grid of cells based on board dimensions
cells = []
for i in range(rows):
    row_idx = []
    for j in range(cols):
        row_idx.append(model.NewBoolVar(f'cell_{i}_{j}'))
    cells.append(row_idx)


regions = {}

# Divide the boards into separate regions based on region id and board
for board_idx in range(len(boards)):
    for row_idx in range(len(boards[board_idx])):
        for col_idx in range(len(boards[board_idx][row_idx])):

            key = f'b{board_idx}_r{boards[board_idx][row_idx][col_idx]}'
            value = cells[row_idx][col_idx]

            if key not in regions:
                regions[key] = []

            regions[key].append(cells[row_idx][col_idx])

print("Regions:", regions)

for i, (region, region_cells) in enumerate(regions.items()):

    left_or_var = model.NewBoolVar('')
    right_or_var = model.NewBoolVar('')
    model.AddBoolXOr([left_or_var, right_or_var])
    model.Add(sum(region_cells) == region_capacity).OnlyEnforceIf(left_or_var)
    model.Add(sum(region_cells) == 0).OnlyEnforceIf(right_or_var)

model.Add(sum([c for row in cells for c in row]) == symbols)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    for i in range(rows):
        for j in range(cols):
            if solver.Value(cells[i][j]):
                print('O', end='')
            else:
                print('_', end='')
        print()

    print("\nCoordinates (row, col): ")
    for i in range(rows):
        for j in range(cols):
            if solver.Value(cells[i][j]):
                print(f'({i},{j})')
else:
    print('No solution found')

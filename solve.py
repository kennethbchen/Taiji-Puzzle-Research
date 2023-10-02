from ortools.sat.python import cp_model
from puzzles import puzzles

selected_puzzle = "test1"
symbols = puzzles[selected_puzzle]["symbols"]
region_capacity = puzzles[selected_puzzle]["region_capacity"]
boards = puzzles[selected_puzzle]["boards"]

rows, cols = len(boards[0]), len(boards[0][0])

model = cp_model.CpModel()

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

for i, (region_id, region_cells) in enumerate(regions.items()):

    for cell in region_cells:
        model.Add(cell == 0).OnlyEnforceIf(len(region_cells) < region_capacity)

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

    print("\nCoordinates (col, row): ")
    for i in range(rows):
        for j in range(cols):
            if solver.Value(cells[i][j]):
                print(f'({j}, {i}),')
else:
    print('No solution found')

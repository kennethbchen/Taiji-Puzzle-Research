from ortools.sat.python import cp_model
from puzzles import puzzles
import time


selected_puzzle = "test2"
symbols = puzzles[selected_puzzle]["symbols"]
region_capacity = puzzles[selected_puzzle]["region_capacity"]
boards = puzzles[selected_puzzle]["boards"]

rows, cols = len(boards[0]), len(boards[0][0])


# ----- Configure Model -----

model = cp_model.CpModel()

"""
# Create grid of cells based on board dimensions
cells = []
for i in range(rows):
    row_idx = []
    for j in range(cols):
        row_idx.append(model.NewBoolVar(f'cell_{i}_{j}'))
    cells.append(row_idx)
"""

# ----- Read Region Data -----
regions = {}
model_vars = {}

# Divide the boards into separate regions based on region id and board

for color_idx in range(len(symbols)):
    for board_idx in range(len(boards)):
        for row_idx in range(len(boards[board_idx])):
            for col_idx in range(len(boards[board_idx][row_idx])):

                # Naming: color(y)_board(x)_region(z)
                region_key = f'b{board_idx}_c{color_idx}_r{boards[board_idx][row_idx][col_idx]}'

                cell_key = (color_idx, board_idx, col_idx, row_idx)

                # Naming: (color, board, col, row)
                value = model.NewBoolVar(str(cell_key))

                if region_key not in regions:
                    regions[region_key] = []

                regions[region_key].append(value)
                model_vars[cell_key] = value

print("Regions:", regions)
print("Model Vars:", model_vars)
exit()
# ----- Configure Model Constraints -----

# Each region (regardless of color) has either [region_capacity] or 0 symbols in it
for i, (region_id, region_cells) in enumerate(regions.items()):

    left_or_var = model.NewBoolVar('')
    right_or_var = model.NewBoolVar('')
    model.AddBoolXOr([left_or_var, right_or_var])
    model.Add(sum(region_cells) == region_capacity).OnlyEnforceIf(left_or_var)
    model.Add(sum(region_cells) == 0).OnlyEnforceIf(right_or_var)

# Each cell (col+row pair) may only have one symbol (of any color) in it

for row_idx in range(len(boards[board_idx])):
    for col_idx in range(len(boards[board_idx][row_idx])):

        pair_cells = []

        for board_idx in range(len(boards)):
            for color_idx in range(len(symbols)):
                pair_cells.append(model_vars[(color_idx, board_idx, col_idx, row_idx)])

        model.Add(sum(pair_cells) <= 1)

# Each colored symbol must appear as many times as defined in symbols

model.Add(sum([c for row in model_vars for c in row]) == symbols)


# ----- Configure Solver -----

""""
class SolutionPrinter(cp_model.CpSolverSolutionCallback):

    # https://developers.google.com/optimization/scheduling/employee_scheduling#python_10

    def __init__(self, cells):
        cp_model.CpSolverSolutionCallback.__init__(self)

        self.cells = cells
        self.__solution_count = 0
        self.__start_time = time.time()

    def on_solution_callback(self):

        current_time = time.time()
        print(
            f"\n---------- Solution {self.__solution_count} ----------\n"
            f"time = {current_time - self.__start_time}s"
        )
        self.__solution_count += 1

        for i in range(rows):
            for j in range(cols):
                if self.Value(cells[i][j]):
                    print('O', end='')
                else:
                    print('_', end='')
            print()

        print("\nCoordinates (col, row): ")

        one_line = ""
        for i in range(rows):
            for j in range(cols):
                if self.Value(cells[i][j]):
                    one_line += f"({j}, {i}), "
                    print(f'({j}, {i}),')
        print("\n")
        print(one_line)
"""
# ----- Solve -----


solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True
# solver.parameters.log_search_progress = True
#solution_printer = SolutionPrinter(cells)

status = solver.Solve(model)

from ortools.sat.python import cp_model
from puzzles import puzzles
import time


selected_puzzle = "8queens"
symbols = puzzles[selected_puzzle]["symbols"]
region_capacity = puzzles[selected_puzzle]["region_capacity"]
boards = puzzles[selected_puzzle]["boards"]

rows, cols = len(boards[0]), len(boards[0][0])


# ----- Configure Model -----

model = cp_model.CpModel()

# Create grid of cells based on board dimensions
cells = []
for i in range(rows):
    row_idx = []
    for j in range(cols):
        row_idx.append(model.NewBoolVar(f'cell_{i}_{j}'))
    cells.append(row_idx)


# ----- Read Region Data -----
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

# ----- Configure Model Constraints -----

for i, (region_id, region_cells) in enumerate(regions.items()):

    for cell in region_cells:
        model.Add(cell == 0).OnlyEnforceIf(len(region_cells) < region_capacity)

    left_or_var = model.NewBoolVar('')
    right_or_var = model.NewBoolVar('')
    model.AddBoolXOr([left_or_var, right_or_var])
    model.Add(sum(region_cells) == region_capacity).OnlyEnforceIf(left_or_var)
    model.Add(sum(region_cells) == 0).OnlyEnforceIf(right_or_var)

model.Add(sum([c for row in cells for c in row]) == symbols)


# ----- Configure Solver -----

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

# ----- Solve -----


solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True
# solver.parameters.log_search_progress = True
solution_printer = SolutionPrinter(cells)

status = solver.Solve(model, solution_printer)

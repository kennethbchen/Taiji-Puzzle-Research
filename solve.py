from ortools.sat.python import cp_model
from puzzles import puzzles
import time
import pandas


selected_puzzle = "test2"
symbols = puzzles[selected_puzzle]["symbols"]
region_capacity = puzzles[selected_puzzle]["region_capacity"]
boards = puzzles[selected_puzzle]["boards"]

rows, cols = len(boards[0]), len(boards[0][0])


# ----- Configure Model -----

model = cp_model.CpModel()

# ----- Read Region Data -----
var_df = pandas.DataFrame(columns=["color", "board", "region_id", "row", "col", "var"])

# Each variable in the model is distinguished by its unique combination of color, board, row, and col
for color_idx in range(len(symbols)):
    for board_idx in range(len(boards)):
        for row_idx in range(len(boards[board_idx])):
            for col_idx in range(len(boards[board_idx][row_idx])):

                row = {}

                var_name = (color_idx, board_idx, col_idx, row_idx)

                row["region_id"] = boards[board_idx][row_idx][col_idx]
                row["board"] = board_idx
                row["color"] = color_idx
                row["col"] = col_idx
                row["row"] = row_idx
                row["var"] = model.NewBoolVar(str(var_name))

                var_df.loc[len(var_df)] = row

print(var_df["var"])
print()
# ----- Configure Model Constraints -----

# Each region (regardless of color) has either [region_capacity] or 0 symbols in it
# Each region can be identified by their unique combination of color, board, and region_id
# cells with the same combination are in the same region
for name, group in var_df.groupby(["color", "board", "region_id"]):

    group_vars = group["var"].tolist()
    print(group)

    left_or_var = model.NewBoolVar('')
    right_or_var = model.NewBoolVar('')
    model.AddBoolXOr([left_or_var, right_or_var])
    model.Add(sum(group_vars) == region_capacity).OnlyEnforceIf(left_or_var)
    model.Add(sum(group_vars) == 0).OnlyEnforceIf(right_or_var)


# Each grid cell (col+row pair) may only have at most one symbol (of any color) in it
for name, group in var_df.groupby(["col", "row"]):

    group_vars = group["var"].tolist()

    model.Add(sum(group_vars) <= 1)

# Each colored symbol must appear as many times as defined in symbols
for name, group in var_df.groupby("color"):

    color_id = group["color"].iloc[0]

    group_vars = group["var"].tolist()

    model.Add(sum(group_vars) == symbols[color_id])




# ----- Configure Solver -----


class SolutionPrinter(cp_model.CpSolverSolutionCallback):

    # https://developers.google.com/optimization/scheduling/employee_scheduling#python_10

    def __init__(self, variables: pandas.DataFrame, rows, cols):
        cp_model.CpSolverSolutionCallback.__init__(self)

        self.variables = variables
        self.rows = rows
        self.cols = cols

        self.__solution_count = 0
        self.__start_time = time.time()




    def on_solution_callback(self):

        current_time = time.time()
        print(
            f"\n---------- Solution {self.__solution_count} ----------\n"
            f"time = {current_time - self.__start_time}s"
        )
        self.__solution_count += 1

        # Get only variables that have a symbol
        df = self.variables
        placements = df[df.apply(lambda val: self.Value(val["var"]) == 1, axis=1)]

        color_map = {}

        for item in placements[["color", "row", "col"]].values:

            color_map[(item[2], item[1])] = item[0]

        one_line = ""
        for r in range(self.rows):
            for c in range(self.cols):

                if (c, r) in color_map:
                    one_line += f"{(c,r)}, "
                    print(color_map[(c, r)], end="")
                else:
                    print("_", end="")
            print()
        print(one_line)

# ----- Solve -----


solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True
solver.parameters.log_search_progress = False
solution_printer = SolutionPrinter(var_df, rows, cols)

status = solver.Solve(model, solution_printer)




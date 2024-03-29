from ortools.sat.python import cp_model
import time
import pandas

def Solve_SGP(puzzle, get_all=False, log_progress=False):
    symbols = puzzle.symbols
    region_capacity = puzzle.region_capacity
    boards = puzzle.boards
    rows, cols = puzzle.board_shape()

    model = cp_model.CpModel()

    # ----- Read Region Data -----
    var_df = pandas.DataFrame(columns=["color", "row", "col", "var"])
    regions = {}

    # Create Variables
    # Each variable in the model is distinguished by its unique combination of color, row, and col
    for color_idx in range(len(symbols)):
        for row_idx in range(len(boards[0])):
            for col_idx in range(len(boards[0][row_idx])):

                row = {}

                var_name = (color_idx, col_idx, row_idx)

                row["color"] = color_idx
                row["col"] = col_idx
                row["row"] = row_idx
                row["var"] = model.NewBoolVar(str(var_name))

                var_df.loc[len(var_df)] = row

    # Read Regions

    # Each region is distinguished by its unique combination of color, board, and region_id
    # cells with the same combination are in the same region
    # For each region in the board, there are as many of that region as there are types of colors
    for color_idx in range(len(symbols)):
        for board_idx in range(len(boards)):
            for row_idx in range(len(boards[board_idx])):
                for col_idx in range(len(boards[board_idx][row_idx])):

                    region_id = boards[board_idx][row_idx][col_idx]

                    region_key = (color_idx, board_idx, region_id)

                    if not region_key in regions:
                        regions[region_key] = []

                    variables = var_df.loc[(var_df["color"] == color_idx) & (var_df["row"] == row_idx) & (var_df["col"] == col_idx), "var"]

                    regions[region_key].append(variables.values[0])


    # ----- Configure Model Constraints -----


    # Each region has either [region_capacity] or 0 symbols in it
    for region_idx, region in enumerate(regions.values()):

        left_or_var = model.NewBoolVar('')
        right_or_var = model.NewBoolVar('')
        model.AddBoolXOr([left_or_var, right_or_var])
        model.Add(sum(region) == region_capacity).OnlyEnforceIf(left_or_var)
        model.Add(sum(region) == 0).OnlyEnforceIf(right_or_var)

    # Each grid cell (col+row pair) may only have at most one symbol (of any color) in it
    for name, group in var_df.groupby(["col", "row"]):

        group_vars = group["var"].tolist()

        model.Add(sum(group_vars) <= 1)

    # Each colored symbol must appear as many times as defined in symbols
    for name, group in var_df.groupby("color"):

        color_id = group["color"].iloc[0]

        group_vars = group["var"].tolist()

        model.Add(sum(group_vars) == symbols[color_id])

    # Solution Hints set constraints on what colors should be in a cell
    for row in range(len(puzzle.solution_hints)):
        for col in range(len(puzzle.solution_hints[0])):

            if puzzle.solution_hints[row][col] != None:
                hint_color = puzzle.solution_hints[row][col] - 1
                hint_var = var_df.query("row=={r} and col=={c} and color=={color}".format(r=row, c=col, color=hint_color))["var"]

                model.Add(hint_var.values[0] == True)



    # ----- Configure Solver -----

    class SolutionCollector(cp_model.CpSolverSolutionCallback):

        # https://stackoverflow.com/questions/58934609/obtain-list-of-sat-solutions-from-ortools

        def __init__(self, variables: pandas.DataFrame, rows, cols):
            cp_model.CpSolverSolutionCallback.__init__(self)

            self.variables = variables
            self.rows = rows
            self.cols = cols

            self.solutions = []

        def on_solution_callback(self):

            # Get only variables that have a symbol
            df = self.variables
            placements = df[df.apply(lambda val: self.Value(val["var"]) == 1, axis=1)]

            self.solutions.append(placements[["row", "col", "color"]])


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

                color_map[(item[2], item[1])] = item[0] + 1

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
    solver.parameters.enumerate_all_solutions = get_all
    solver.parameters.log_search_progress = log_progress
    solution_callback = SolutionCollector(var_df, rows, cols)

    status = solver.Solve(model, solution_callback)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

        if solver.parameters.enumerate_all_solutions:
            return solution_callback.solutions
        else:
            # Get only variables that were used in the solution
            return [var_df[var_df["var"].apply(lambda var: solver.Value(var) == 1)][["row", "col", "color"]]]

    else:
        return []

class SGP():
    def __init__(self, symbols, boards, solution_hints=[], region_capacity=2, diagonals_allowed=False):

        self.symbols = symbols

        self.boards = boards

        self.solution_hints = solution_hints

        self.region_capacity = region_capacity

        self.diagonals_allowed = diagonals_allowed

    def __str__(self):
        output = "Symbols: {sym}\nRegion Capacity: {rc}\nDiagonals Allowed: {da}\nBoards:\n{bds}\n"
        return output.format(sym=self.symbols, rc=self.region_capacity, da=self.diagonals_allowed, bds=self.boards)

    def num_colors(self):
        return len(self.symbols)

    def num_boards(self):
        return len(self.boards)

    # row, col
    def board_shape(self):
        return len(self.boards[0]), len(self.boards[0][0])

    @staticmethod
    def from_dict(data_dict):
        symbols = data_dict["symbols"]
        rc = data_dict["region_capacity"]
        boards = data_dict["boards"]
        diag_allowed = data_dict["diagonals"] if "diagonals" in data_dict else False

        return SGP(symbols, boards, region_capacity=rc, diagonals_allowed=diag_allowed)
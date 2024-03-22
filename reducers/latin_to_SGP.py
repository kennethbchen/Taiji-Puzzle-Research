import numpy
from sudoku import Sudoku

from SGP import SGP
import numpy as np

# latin_square should be some nxn numpy array filled with numbers [1, n-1]
# latin_square can be partially filled if certain values are None
def latin_to_SGP(latin_square_array):
    latin_square_size = latin_square_array.shape[0]
    sgp_size = latin_square_array.shape[0] * 2

    # Array of 4 boards where each number in a board is a distinct region
    sgp_boards = np.zeros((4, sgp_size, sgp_size), dtype=int)

    # Columns
    sgp_boards[1] = np.full( (sgp_size, sgp_size), np.arange(0, sgp_size))

    # Rows
    sgp_boards[0] = np.transpose(sgp_boards[1])

    # Horizontal checkerboard (2 columns, 1 row)

    row_id_offset = np.arange(0, latin_square_size).repeat(2).reshape(1, -1).repeat(sgp_size, 0)
    col_id_offset = np.arange(0, sgp_size * latin_square_size, latin_square_size).repeat(sgp_size).reshape((sgp_size, -1))

    sgp_boards[2] = row_id_offset + col_id_offset

    sgp_boards[3] = sgp_boards[2].transpose()

    # Symbols
    sgp_symbols = np.full(latin_square_size, latin_square_size * 4).tolist()

    sgp_hint = tile_latin_square_array(latin_square_array)

    return SGP(sgp_symbols, sgp_boards.tolist(), solution_hints=sgp_hint)

# Takes an existing latin square and returns an array that represents how that latin square would look like
# as an SGP
def tile_latin_square_array(latin_square_array):
    return np.array(latin_square_array).repeat(2, 1).repeat(2, 0)

# Takes a tiled SGP solution of a latin square and converts it to a latin square
def untile_sgp_solution_array(tiled_lsa):
    return tiled_lsa[0: len(tiled_lsa): 2, 0: len(tiled_lsa[0]): 2]
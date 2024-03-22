import numpy
from sudoku import Sudoku

from SGP import SGP
import numpy as np

# latin_square should be some nxn numpy array filled with numbers [1, n-1]
# latin_square can be partially filled if certain values are None
def latin_to_SGP(latin_square_array):
    latin_square_size = latin_square_array.shape[0]
    sgp_size = latin_square_array.shape[0] * 2
    print(latin_square_size, sgp_size)

    # Array of 4 boards where each number in a board is a distinct region
    sgp_boards = np.zeros((4, sgp_size, sgp_size), dtype=int)

    # Columns
    sgp_boards[1] = np.full( (sgp_size, sgp_size), np.arange(0, sgp_size))

    # Rows
    sgp_boards[0] = np.transpose(sgp_boards[1])

    # Horizontal checkerboard (2 columns, 1 row)

    row_id_offset = np.zeros( (sgp_size, latin_square_size, 2)) + np.arange(0, latin_square_size).reshape((latin_square_size, -1))
    row_id_offset = row_id_offset.reshape((sgp_size, -1))
    col_id_offset = np.zeros( (sgp_size, sgp_size) ) + np.arange(0, sgp_size * latin_square_size, latin_square_size).reshape((sgp_size, 1))

    sgp_boards[2] = row_id_offset + col_id_offset

    sgp_boards[3] = sgp_boards[2].transpose()

    # Symbols
    sgp_symbols = np.full(latin_square_size, latin_square_size * 4).tolist()

    sgp_hint = np.tile(np.array(latin_square_array), (2, 2))

    print(sgp_boards)
    return SGP(sgp_symbols, sgp_boards.tolist())


def get_solution_tile(solution, tile=(0, 0)):
    # Assumes rectangular solution size

    # (row, col)
    tile_size = (int(len(solution) / 2), int(len(solution[0]) / 2))

    tile_offset = (tile[0] * tile_size[0], tile[1] * tile_size[1])

    return solution[tile_offset[0]: (tile_offset[0] + tile_size[0]), tile_offset[1]: (tile_offset[1] + tile_size[1])]


def is_solution_tiled(solution):
    # Assumes rectangular solution size

    # (row, col)
    tile_size = (int(len(solution)/2), int(len(solution[0])/2))

    tile_positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

    origin_tile = None
    for tile in tile_positions:

        current_tile_data = get_solution_tile(solution, tile)

        if origin_tile is None:
            origin_tile = current_tile_data

        if not (current_tile_data == origin_tile).all():

            """
            print("Origin tile and", tile, "are not the same")
            print(origin_tile)
            print("vs")
            print(current_tile_data)
            """
            return False

    return True

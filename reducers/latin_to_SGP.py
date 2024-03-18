import numpy
from sudoku import Sudoku

from SGP import SGP
import numpy as np

def latin_to_SGP(sudoku_puzzle):
    sgp_size = sudoku_puzzle.size * 2
    # Array of 4 boards where each number in a board is a distinct region
    sgp_boards = np.zeros((4, sgp_size, sgp_size))

    # Columns
    sgp_boards[1] = np.full( (sgp_size, sgp_size), np.arange(0, sgp_size))

    # Rows
    sgp_boards[0] = np.transpose(sgp_boards[1])

    # Symbols
    sgp_symbols = np.full((sudoku_puzzle.width * sudoku_puzzle.height), sudoku_puzzle.width * sudoku_puzzle.height * 4).tolist()

    sgp_hint = np.tile(np.array(sudoku_puzzle.board), (2,2))

    return SGP(sgp_symbols, sgp_boards.tolist(), solution_hints=sgp_hint)


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

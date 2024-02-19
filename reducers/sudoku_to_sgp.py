import numpy
from sudoku import Sudoku

from SGP import SGP
import numpy as np

def sudoku_to_SGP(sudoku_puzzle):
    print(sudoku_puzzle)
    sgp_size = sudoku_puzzle.size * 2
    # Array of 4 boards where each number in a board is a distinct region
    sgp_boards = np.zeros((4, sgp_size, sgp_size))

    # Columns
    sgp_boards[1] = np.full( (sgp_size, sgp_size), np.arange(0, sgp_size))

    # Rows
    sgp_boards[0] = np.transpose(sgp_boards[1])


    # n x m blocks

    # Vertical Checkerboard

    # Dimensions of a checkerboard where the grid height > width
    v_check_rows = int(sgp_size / sudoku_puzzle.height / 2)
    v_check_height = sudoku_puzzle.height * 2
    v_check_cols = sgp_size
    v_check_width = sudoku_puzzle.width

    checker_col = np.zeros(( v_check_rows, v_check_height, v_check_cols))

    checker_col = checker_col.reshape(v_check_rows, v_check_cols * v_check_height)

    # Add checkerboard row id offset
    checker_col += np.arange(0, v_check_cols, v_check_height).reshape(v_check_rows, -1)

    checker_col = checker_col.reshape(v_check_rows, v_check_height, v_check_cols)

    # Add checkerboard column id offset
    temp = np.broadcast_to(np.arange(0, v_check_cols / v_check_width).reshape(-1, 1), ( int(v_check_cols / v_check_width) , v_check_width)).flatten()

    checker_col = (checker_col + temp).reshape(sgp_size, sgp_size)

    sgp_boards[2] = checker_col

    # Horizontal Checkerboard
    sgp_boards[3] = np.transpose(checker_col)

    # Symbols
    sgp_symbols = np.full((sudoku_puzzle.width * sudoku_puzzle.height), sudoku_puzzle.width * sudoku_puzzle.height).tolist()

    sgp_hint = np.tile(np.array(sudoku_puzzle.board), (2,2))

    return SGP(sgp_symbols, sgp_boards.tolist(), solution_hints=sgp_hint)

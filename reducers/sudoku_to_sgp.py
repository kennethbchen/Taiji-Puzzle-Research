import numpy
from sudoku import Sudoku

from SGP import SGP
import numpy as np

puzzle = Sudoku(3).difficulty(0.5)

def sudoku_to_SGP(sudoku_puzzle):

    sgp_size = sudoku_puzzle.size * 2
    # Array of 4 boards where each number in a board is a distinct region
    sgp_boards = np.zeros((4, sgp_size, sgp_size))

    # Columns
    sgp_boards[1] = np.full( (sgp_size, sgp_size), np.arange(0, sgp_size))

    # Rows
    sgp_boards[0] = np.transpose(sgp_boards[1])


    # n x m blocks


    print(sudoku_puzzle)
    print(sgp_size)
    print(sgp_boards)
    #print(sgp_boards.tolist())

    sgp_hint = np.tile(np.array(sudoku_puzzle.board), (2,2))



sudoku_to_SGP(puzzle)
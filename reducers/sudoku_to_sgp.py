from sudoku import Sudoku

from SGP import SGP
import numpy as np

puzzle = Sudoku(2,2).difficulty(0.5)

def sudoku_to_SGP(sudoku_puzzle):
    #print(sudoku_puzzle)

    # Arrays of boards where each number is a distinct region
    sgp_boards = []

    # Rows
    sgp_boards.append(np.transpose(np.full( (sudoku_puzzle.size, sudoku_puzzle.size), np.arange(0, sudoku_puzzle.size))))

    # Columns
    sgp_boards.append(np.transpose(sgp_boards[0]))

    # Diagonals


    print(sudoku_puzzle)
    print(sudoku_puzzle.height, sudoku_puzzle.width)
    print(sgp_boards)

    sgp_hint = np.tile(np.array(sudoku_puzzle.board), (2,2))



sudoku_to_SGP(puzzle)
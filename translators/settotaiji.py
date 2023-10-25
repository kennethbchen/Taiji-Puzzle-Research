import pprint

uni = [1, 2, 3, 4]
sts = [[1, 3], [2, 4], [1], [2, 3, 4]]

def print_board(board):
    for row in board:
            print(row)

def set_to_taiji(universe, subsets):

    rows = 3
    cols = len(subsets) * 3

    boards = []

    """
        Create Helper Boards
        These boards make it impossible for certain squares to be a part of the taiji solution.
        It does it by having at least one layer where it is a region of size one, making pairing impossible.
        
        The goal is to keep each square with a letter in it (below) a valid solution, while blocking all others
        
        Create Constraint For Boards:
        
        C1A:
        A X _ B X _
        A _ _ B _ _ ...
        _ _ _ _ _ _
        
        C1B:
        A _ _ B _ _
        A X _ B X _ ...
        _ _ _ _ _ _
        
        C2A:
        A _ X B _ X
        A _ _ B _ _ ...
        _ _ _ _ _ _
        
        C2B:
        A _ _ B _ _
        A _ X B _ X ...
        _ _ _ _ _ _
        
        C3:
        A _ _ B _ _
        A _ _ B _ _ ...
        X X X X X X
    """

    c1a = []
    c1b = []
    c2a = []
    c2b = []
    c3 = []
    for row in range(rows):

        c1a_row_data = []
        c1b_row_data = []
        c2a_row_data = []
        c2b_row_data = []
        c3_row_data = []
        for col in range(cols):

            # C1
            if (col // 3) % 2 == 0:
                c1a_row_data.append(0)
                c1b_row_data.append(0)
            else:
                c1a_row_data.append(1)
                c1b_row_data.append(1)

            # A
            if row == 0:
                if (col - 1) % 3 == 0:
                    # Flip 0 <-> 1
                    c1a_row_data[col] = 1 if c1a_row_data[col] == 0 else 0

            # B
            if row == 1:
                if (col - 1) % 3 == 0:
                    c1b_row_data[col] = 1 if c1b_row_data[col] == 0 else 0

            # C2
            if ((col - 1) // 3) % 2 == 0:
                c2a_row_data.append(1)
                c2b_row_data.append(1)
            else:
                c2a_row_data.append(0)
                c2b_row_data.append(0)

            # A
            if row == 0:
                if (col + 1) % 3 == 0:
                    c2a_row_data[col] = 1 if c2a_row_data[col] == 0 else 0
            # B
            if row == 1:
                if (col + 1) % 3 == 0:
                    c2b_row_data[col] = 1 if c2b_row_data[col] == 0 else 0

            # C3
            if row == 0 or row == 1:
                if col % 2 == 0:
                    c3_row_data.append(1)
                else:
                    c3_row_data.append(0)
            else:
                if col % 2 == 0:
                    c3_row_data.append(0)
                else:
                    c3_row_data.append(1)

        c1a.append(c1a_row_data)
        c1b.append(c1b_row_data)

        c2a.append(c2a_row_data)
        c2b.append(c2b_row_data)

        c3.append(c3_row_data)

    boards.append(c1a)
    boards.append(c1b)

    boards.append(c2a)
    boards.append(c2b)

    boards.append(c3)

    # Create constraints for the sets
    for data in subsets:
        set_board = [[0 for col in range(cols)] for row in range(rows)]

        not_set = list(set(universe) - set(data))

        # Separate everything that is not in data into its own region
        for item in not_set:
            col = (item - 1) * 3

            set_board[0][col] = 1
            set_board[1][col] = 1

        boards.append(set_board)

    return boards

class CSP_SudokuConstraintChecker:
    """
    A class to check constraints on a Sudoku board using the CSP (Constraint Satisfaction Problem) approach.

    This class provides methods for validating a Sudoku board by checking its rows, columns, 3x3 sub-squares,
    and individual positions to ensure they meet the standard Sudoku constraints.

    Attributes
    ----------
    board_state : list of list of int
        The current state of the Sudoku board represented as a 9x9 2D list of integers (0 represents an empty cell).
    constraint_approach : object
        An instance of a constraint-solving approach that is used to solve the board.
    verbose : bool, optional
        A flag that controls whether to print detailed logs during the solving process. Default is False.

    Methods
    -------
    solver():
        Initiates the solving process for the current Sudoku board and returns the solved board.
    check_subSquare(row, column, board_state):
        Checks if the 3x3 sub-square starting at the specified (row, column) is valid.
    check_line(line):
        Checks if a row, column, or 3x3 sub-square contains no duplicate values.
    check_axes(board_state, axis, axis_index, num):
        Checks if the number `num` is valid in the specified row or column.
    check_ifUsed(board_state, row, column, num):
        Checks if a number is already used in the 3x3 sub-square that contains the specified (row, column).
    check_done(board_state):
        Checks if the Sudoku board is completely solved.
    check_coords(arr, row, column, num):
        Verifies if a number can be placed at a specific position on the Sudoku board.
    check_conflicts(board_state, row, column, num):
        Identifies conflicts in the board when placing a number at the specified position.
    """
    def __init__(self, board_state, constraint_approach, verbose=False):
        """
        Initializes the Sudoku constraint checker with the current board state,
        constraint-solving approach, and verbosity option.

        Parameters
        ----------
        board_state : list of lists of int
            The current state of the Sudoku board as a 2D list.
        constraint_approach : object
            The object or approach to be used for solving the Sudoku with constraints.
        verbose : bool, optional
            If True, prints detailed logs for the solving process (default is False).
        """
        self.verbose = verbose
        self.board_state = board_state
        self.constraint_approach = constraint_approach

    def solver(self):
        """
        Initiates the solving process for the current Sudoku board.

        This method generates a list of coordinates for empty cells (cells with value 0) 
        on the board and then calls the constraint-solving method to attempt filling in 
        the Sudoku grid according to the constraints.

        Returns
        -------
        list
            A list representing the solved Sudoku board or an empty list if no solution is found.
        """
        # Generate coordinates for all empty cells in the 9x9 Sudoku grid
        coords = [(x, y) for x in range(9) for y in range(9) if self.board_state[x][y] == 0]
        
        # Calls the constraint-based solver with the current board state
        return self.constraint_approach.solver(self)

    def check_subSquare(self, row, column, board_state):
        """
        Checks if a 3x3 sub-square in the Sudoku board is valid.

        This function extracts a 3x3 sub-square from the Sudoku board starting at the specified 
        row and column coordinates. It then checks if the values within this sub-square follow 
        the Sudoku rules, ensuring no repeated numbers from 1 to 9.

        Parameters
        ----------
        row : int
            The starting row index for the 3x3 sub-square.
        column : int
            The starting column index for the 3x3 sub-square.
        board_state : list of list of int
            The current state of the Sudoku board, represented as a 2D list or array.

        Returns
        -------
        bool
            True if the 3x3 sub-square follows Sudoku rules (no duplicates), False otherwise.
        """
        # Extract the 3x3 sub-square values starting from (row, column)
        sub_square = [board_state[(row + x), (column + y)] for x in range(3) for y in range(3)]
        
        # Check if the extracted 3x3 square is valid using checkLine
        return self.check_line(sub_square)


    def check_line(self, line):
        """
        Checks if a line (row, column, or sub-square) in the Sudoku board is valid.

        This function verifies that there are no duplicate numbers in the provided line,
        ignoring zeros (which represent empty cells). It uses a set to ensure that
        the unique numbers (excluding zeros) match the count of non-zero entries in the line.

        Parameters
        ----------
        line : list of int
            A list representing a row, column, or 3x3 sub-square from the Sudoku board.

        Returns
        -------
        bool
            True if the line has no duplicates among the non-zero entries, False otherwise.
        """
        # Convert line to a set, excluding zeros, and check if its length matches non-zero count in line
        return len(set(line) - {0}) == len(line) - line.count(0)


    def check_axes(self, board_state, axis, axis_index, num):
        """
        Checks if a given number is valid within a specified row or column of the Sudoku board.

        This function determines if `num` already exists in the specified row or column,
        which is crucial for maintaining Sudoku's constraint of unique numbers in each row and column.

        Parameters
        ----------
        board_state : list of lists of int
            Current state of the Sudoku board as a 2D list.
        axis : int
            Indicates which axis to check (0 for row, 1 for column).
        axis_index : int
            The index of the row or column to be checked.
        num : int
            The number to check for validity in the specified row or column.

        Returns
        -------
        bool
            True if `num` is already present in the specified row or column, False otherwise.
        """
        # Verbose output if enabled, indicating the number and axis being checked
        if self.verbose:
            print(f"Checking if {num} is valid in {'row' if axis == 0 else 'column'} {axis_index}")

        # Check each element in the specified row or column for the presence of `num`
        return any(board_state[axis_index][x] == num if axis == 0 else board_state[x][axis_index] == num for x in range(9))


    def check_ifUsed(self, board_state, row, column, num):
        """
        Checks if a specified number already exists within a 3x3 sub-square of the Sudoku board.

        This function ensures that `num` is not duplicated within a 3x3 sub-square,
        as per Sudoku rules, by examining each cell in the sub-square that contains
        the cell located at the given `row` and `column`.

        Parameters
        ----------
        board_state : list of lists of int
            Current state of the Sudoku board as a 2D list.
        row : int
            The starting row index of the 3x3 sub-square.
        column : int
            The starting column index of the 3x3 sub-square.
        num : int
            The number to check for within the specified 3x3 sub-square.

        Returns
        -------
        bool
            True if `num` is found within the specified 3x3 sub-square, False otherwise.
        """
        # Check each cell in the 3x3 sub-square for the presence of `num`
        return any(board_state[x + row][y + column] == num for x in range(3) for y in range(3))


    def check_done(self, board_state):
        """
        Checks if the Sudoku board has been fully solved.

        This function verifies if the current board satisfies the rules of Sudoku, meaning:
        - All rows are valid (no duplicates).
        - All columns are valid (no duplicates).
        - All 3x3 sub-squares are valid (no duplicates).
        - There are no empty cells (represented by 0).

        Parameters
        ----------
        board_state : list of lists of int
            Current state of the Sudoku board as a 2D list.

        Returns
        -------
        bool
            True if the board is completely solved (all rows, columns, and sub-squares are valid, and there are no empty cells), False otherwise.
        """
        # Check that all rows, columns, and sub-squares are valid, and there are no empty cells
        axis_index = 1
        return all(
            self.check_line(board_state[axis_index, :]) and  # Validate each row
            self.check_line(board_state[:, axis_index]) and  # Validate each column
            self.check_subSquare(int(x / 3) * 3, (x % 3) * 3, board_state)  # Validate each 3x3 sub-square
            for x in range(9)
        ) and 0 not in board_state  # Ensure there are no empty cells in the board (0)


    def check_coords(self, arr, row, column, num):
        """
        Checks if a number can be placed in a specific position on the Sudoku board.

        This function verifies that a given number is not already present in:
        - The 3x3 sub-square that contains the specified position.
        - The row that contains the specified position.
        - The column that contains the specified position.

        Parameters
        ----------
        arr : list of lists of int
            The current state of the Sudoku board as a 2D list.
        row : int
            The row index where the number is to be placed.
        column : int
            The column index where the number is to be placed.
        num : int
            The number to be checked for placement.

        Returns
        -------
        bool
            True if the number can be placed in the specified position (i.e., it is not already in the row, column, or sub-square), 
            False otherwise.
        """
        # Check that the number is not already used in the 3x3 sub-square
        # and not in the same row or column.
        return not self.check_ifUsed(arr, row - row % 3, column - column % 3, num) and \
               not self.check_axes(arr, 0, row, num) and \
               not self.check_axes(arr, 1, column, num)


    def check_conflicts(self, board_state, row, column, num):
        """
        Checks for conflicts in the Sudoku board when attempting to place a number at a specific position.

        This function identifies all the positions on the Sudoku board where the specified number already 
        exists in the same row, column, or 3x3 sub-square, and returns those positions as a set of conflicts.

        Parameters
        ----------
        board_state : list of lists of int
            The current state of the Sudoku board as a 2D list.
        row : int
            The row index where the number is to be placed.
        column : int
            The column index where the number is to be placed.
        num : int
            The number to be checked for conflicts.

        Returns
        -------
        set
            A set containing the positions (row, column) where the number already exists, 
            including the row, column, and 3x3 sub-square.
        """
        # Initialize an empty set to store conflicts.
        conflict_set = {(row + (x * 8)) for x in range(9) if board_state[row][x] == num}
        
        # Add conflicts from the same column.
        conflict_set.update((x + (column * 8)) for x in range(9) if board_state[x][column] == num)

        # Identify the 3x3 sub-square where the position (row, column) belongs.
        box_row, box_column = row - row % 3, column - column % 3

        # Add conflicts from the 3x3 sub-square.
        conflict_set.update(x + box_row + (8 * (y + box_column)) for x in range(3) for y in range(3) if board_state[x + box_row][y + box_column] == num)

        # Add the current position as a conflict.
        conflict_set.add(row + (8 * column))

        return conflict_set

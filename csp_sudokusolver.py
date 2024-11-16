from csp_utils import CSP_utils
from itertools import islice

class CSP_SudokuSolver:
    """
    A class to solve a Sudoku puzzle using the Backjumping algorithm within the CSP (Constraint Satisfaction Problem) framework.

    This class provides methods to iteratively try different numbers in empty Sudoku cells and backtrack when conflicts are found.
    The solving process is controlled by verbosity levels to track the algorithm's progress in different levels of detail.

    Attributes
    ----------
    verbose : bool
        A flag that controls whether detailed logs are printed during the solving process.
    verbose_level : int
        A value to control the level of detail of the logs printed. Higher values produce more detailed logs.
    iteration_level : int
        Defines the frequency at which the iteration details are printed.
    iteration_count : int
        Counter to track the number of iterations in the backjumping process.

    Methods
    -------
    solver(sudoku):
        Solves the Sudoku puzzle by calling the backjumping_algorithm method with the current state of the board.
    backjumping_algorithm(sudoku, board_state, coords):
        Solves the puzzle using the backjumping technique, attempting to assign values to cells and handling conflicts.
    try_value(sudoku, board_state, x, row_after, column_after, coords_after):
        Attempts to place a value in a specified cell and propagates the backjumping algorithm.
    """

    def __init__(self, verbose=False, verbose_level=1, iteration_level=10):
        """
        Initialize the CSP_SudokuSolver object with the provided verbosity settings and counters.

        Parameters
        ----------
        verbose : bool, optional
            print detailed logs during the solving process. Default is False.
        verbose_level : int, optional
            The verbosity level that controls the amount of output generated during solving. Default is 1.
        iteration_level : int, optional
            Defines how often iteration details are printed. Default is 10 (prints every 10 iterations).
        """
        self.verbose = verbose
        self.verbose_level = verbose_level
        self.iteration_level = iteration_level
        self.iteration_count = 0

    def solver(self, sudoku):
        """
        Solves the Sudoku puzzle using the Backjumping algorithm.

        Parameters
        ----------
        sudoku : object
            An instance of the Sudoku puzzle object containing the board state and methods to check constraints.

        Returns
        -------
        tuple
            A tuple containing two elements: 
            - A boolean indicating if the puzzle was solved (True or False).
            - The updated board state after attempting to solve.
        """
        coords = [(x, y) for x in range(9) for y in range(9) if sudoku.board_state[x][y] == 0]
        solved, board_state, _ = self.backjumping_algorithm(sudoku, sudoku.board_state, coords)

        if solved:
            print("\nSudoku solved:\n")
            CSP_utils.print_board(board_state, self.verbose)
        else:
            print("No solution found.")
        
        return solved, board_state

    def backjumping_algorithm(self, sudoku, board_state, coords):
        """
        Performs the Backjumping algorithm to try to fill the Sudoku board with valid numbers.

        The algorithm attempts to place values in empty cells and backtracks when a conflict is encountered.
        It also tracks conflicts during the process and removes them as needed.
        
        Based in the pseudo-code and graphs of:
            Dechter, R., & Frost, D. (2002). Backjump-based backtracking for constraint satisfaction problems. Artificial Intelligence.

        Parameters
        ----------
        sudoku : object
            An instance of the Sudoku puzzle object containing the board state and methods to check constraints.
        board_state : list of list of int
            The current state of the Sudoku board represented as a 2D list (0 for empty cells).
        coords : list of tuple of int
            A list of coordinates (row, column) representing the empty cells that need to be filled.

        Returns
        -------
        tuple
            A tuple containing:
            - A boolean indicating if the puzzle was solved
            - The updated board state after that the algorithm was applying.
            - A set of conflicts encountered during the solving process.
        """
        # Verbose detail level 1 (default)
        if self.verbose and self.verbose_level == 1:
            self.iteration_count += 1
            if self.iteration_count % self.iteration_level == 0:
                print(f"[Iteration: {self.iteration_count}] Backjump called with coords: \n{coords}\n")

        # Base-case
        if not coords:
            return True, board_state, set()

        conflict_set = set()
        row_after, column_after = coords[0]
        coords_after = list(islice(coords, 1, None)) # coordinates remaining after current

        # place each number from 1 to 9 in the specified cell   
        for x in range(1, 10):
            # Calling of method try_value
            result, update_puzzle, new_conflicts = self.try_value(sudoku, board_state, x, row_after, column_after, coords_after)

            # Level 2 of verbose detail
            if self.verbose and self.verbose_level == 2 and self.iteration_count % self.iteration_level == 0:
                if x % 3 == 0:
                    self.iteration_count += 1
                    print(f"[Iteration: {self.iteration_count}]\nTrying value {x} at ({row_after}, {column_after}) - Result: {'Success' if result else 'Failure'}\n")

            if result:
                return True, update_puzzle, set()
            elif (row_after + (8 * column_after)) not in new_conflicts:
                return False, board_state, new_conflicts
            else:
                new_conflicts.remove(row_after + (8 * column_after))
                conflict_set = conflict_set.union(new_conflicts)

            board_state[row_after, column_after] = 0

        # Level 3 of verbose detail
        if self.verbose and self.verbose_level == 3 and conflict_set and self.iteration_count % self.iteration_level == 0:
            self.iteration_count += 1
            print(f"[Iteration: {self.iteration_count}]\nTrying value {x} at ({row_after}, {column_after}) - Result: {'Success' if result else 'Failure'}\nConflicts at ({row_after}, {column_after}): whit value {x}\nTotal conflicts - {len(conflict_set)}\n")

        # If none of the values ​​from 1 to 9 were valid, we returned False with the conflicts found
        return False, board_state, conflict_set

    def try_value(self, sudoku, board_state, x, row_after, column_after, coords_after):
        """
        Attempts to place a value in a specified cell on the Sudoku board and propagates the backjumping algorithm.

        Parameters
        ----------
        sudoku : object
            An instance of the Sudoku puzzle object containing the board state and methods to check constraints.
        board_state : list of list of int
            The current state of the Sudoku board represented as a 2D list (0 for empty cells).
        x : int
            The value to try placing in the specified cell.
        row_after : int
            The row index of the cell to place the value in.
        column_after : int
            The column index of the cell to place the value in.
        coords_after : list of tuple of int
            A list of remaining empty cell coordinates to process after placing the value.

        Returns
        -------
        tuple
            A tuple containing:
            - A boolean indicating if the value placement was successful (True or False).
            - The updated board state after attempting the placement.
            - A set of conflicts encountered during the process.
        """
        if sudoku.check_coords(board_state, row_after, column_after, x):
            board_state[row_after, column_after] = x
            return self.backjumping_algorithm(sudoku, board_state.copy(), coords_after)
        else:
            return False, board_state, sudoku.check_conflicts(board_state, row_after, column_after, x)
   

    def is_valid_solution(self, board_state):
        """
        verify if the solution of the board is valid
        
        check that the rows, columns and subframes (3x3) have the numbers
        between 1 and 9 whithout repeating.
        
        Parameters
        ----------
        board_state : list of list of int
            The actual state of the sudoku board
        
        Returns
        -------
        bool
            true if the board is valid, false if not.
        """
        # Verify rows
        for row in range(9):
            if not self.is_valid_group(board_state[row]):
                print(f"Fila {row} no válida.")
                return False

        # Verify columns
        for col in range(9):
            column = [board_state[row][col] for row in range(9)]
            if not self.is_valid_group(column):
                print(f"Columna {col} no válida.")
                return False

        # Verificar subgrid 3x3
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [board_state[row][col] for row in range(box_row, box_row + 3) for col in range(box_col, box_col + 3)]
                if not self.is_valid_group(box):
                    print(f"Subcuadro 3x3 en ({box_row}, {box_col}) no válido.")
                    return False

        return True

    def is_valid_group(self, group):
        """
        Checks if a group of elements (row, column or subbox) is valid,
        that is, if it contains all the numbers from 1 to 9 without repeating itself.
        
        Parameters
        ----------
        group : list 
            The list of numbers to check.
        
        Returns
        -------
        bool
            True if the group is valid, False if not.
        """
        return sorted(group) == list(range(1, 10))

from csp_sudokusolver import CSP_SudokuSolver
from csp_sudokuconstraintchecker import CSP_SudokuConstraintChecker
from csp_utils import CSP_utils
import numpy as np
import os

# Store compilation arguments.
args = CSP_utils.parse_args()

# Compilation arguments
verbose = args.verbose
verbose_level = args.verbose_level
iteration_level = args.iteration_level

# Detects the path of the main file
base_dir = os.path.dirname(os.path.abspath(__file__)) 
BOARDCODE = args.boardcode
FILENAME = os.path.join(base_dir, 'boards', BOARDCODE)


# Print the compiling information
CSP_utils.print_info(verbose,verbose_level, iteration_level,BOARDCODE, FILENAME)

def main():
    """
    Main function that initiates the Sudoku-solving process.
    
    This function reads the Sudoku board from the specified file, creates the solver 
    and constraint checker instances, and solves the puzzle. If verbose mode is active,
    it will display the initial board before solving.
    """
    # Read the Sudoku board from the file
    board = read_sudoku_from_file(FILENAME)
    
    # Initialize constraint checker and solver with specified verbosity and iteration level
    sudoku = CSP_SudokuConstraintChecker(board, CSP_SudokuSolver(verbose, verbose_level, iteration_level))
    
    # Solve the Sudoku puzzle and store the final board
    final_board = solve_sudoku(sudoku)
    
    # Print the initial board if verbose mode is enabled
    if verbose:
        print("\nInitial board:\n")
        CSP_utils.print_board(board, verbose)
    
    # print("\nResolved Sudoku Board:")
    # print(final_board)
    
    # board = read_sudoku_from_file(FILENAME)
    # solver = CSP_SudokuSolver(verbose=True, verbose_level=1, iteration_level=100)
    # sudoku = CSP_SudokuConstraintChecker(board, CSP_SudokuSolver(verbose, verbose_level, iteration_level))

    # solved, board_state = solver.solver(sudoku)

    # if solver.is_valid_solution(board_state):
    #     print("La solución es válida.")
    # else:
    #     print("La solución no es válida.")


def read_sudoku_from_file(filename):
    """
    Reads a Sudoku board from a specified file and converts it to a NumPy array.
    
    Parameters
    ----------
    filename : str
        Path to the Sudoku board file.
        
    Returns
    -------
    np.ndarray
        The Sudoku board represented as a NumPy array.
    """
    with open(filename) as file:
        # Read each line, split by commas, and convert to integers
        board = [list(map(int, line.strip().split(','))) for line in file]
    return np.array(board)


def solve_sudoku(sudoku):
    """
    Solves the Sudoku puzzle using the provided solver and returns the solved board as a list.
    
    Parameters
    ----------
    sudoku : CSP_SudokuConstraintChecker
        An instance of the Sudoku constraint checker containing the solver method.
        
    Returns
    -------
    list
        The solved Sudoku board in the form of a Python list.
    """
    # Call the solver method to get the solved board
    solved_board = sudoku.solver()[1]  # Directly retrieves the solved Sudoku board
    return solved_board.tolist()  # Converts the solved board to a Python list format


if __name__ == '__main__':
    main()

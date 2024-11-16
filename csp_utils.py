import argparse
import os

class CSP_utils:
    """
    Utility class containing helper methods for solving Sudoku using the backjumping algorithm.
    This includes methods for parsing command-line arguments, printing Sudoku boards,
    and displaying information about the solving process.
    """

    def parse_args():
        """
        Parses command-line arguments to configure the Sudoku solver.

        Returns
        -------
        argparse.Namespace
            The parsed arguments containing configuration parameters.
        """
        # Create the object ArgumentParser for input parameters
        parser = argparse.ArgumentParser(description="Expert level Sudoku solver using backjumping")
        
        # Add an optional argument '--verbose' for toggle verbose
        parser.add_argument('--verbose', action='store_true', help='Activate detailed output')
        
        # Add argument '--verbose_level' for verbose level detail (1, 2, 3)
        parser.add_argument('--verbose-level', type=int, default=1, help='Verbosity level: \n1: simplified verbosity \n2: intermediate verbosity \n3: complete verbosity \n(1-3) [Default: 1]')
        
        # Add argument '--iteration_level' that define the number of iteration
        parser.add_argument('--iteration-level', type=int, default=10, help='Number of iterations between verbose outputs [Default: 10]')
        
        # Add argument '--boardcode' to specify the name of the board-game
        parser.add_argument('--boardcode', type=str, default='DG9TFMNR.txt', help='Sudoku board file name to solve [Default: DG9TFMNR.txt]')
        
        # Parsed args
        return parser.parse_args()

    
    def print_info(verbose, verbose_level, iteration_level, BOARDCODE, FILENAME):
        """
        Prints the initial information about the Sudoku solver configuration.

        Parameters
        ----------
        verbose : bool
            Whether verbose output is enabled or not.
        verbose_level : int
            The verbosity level (1, 2, or 3).
        iteration_level : int
            The number of iterations between verbose outputs.
        BOARDCODE : str
            The name of the file containing the Sudoku board to solve.
        FILENAME : str
            The path to the file containing the Sudoku board.
        """
        # Print config info
        print(f"\nBoard path: {FILENAME}")
        print(f"Reading board: {BOARDCODE}")
        if verbose:
            print(f"Verbose: {verbose}")
            print(f"Verbose Level: {verbose_level}")
            print(f"Iteration Level: {iteration_level}")
    
    def print_board(board, verbose):
        """
        Prints the Sudoku board in a readable format.

        Parameters
        ----------
        board : list of list of int
            The current state of the Sudoku board.
        verbose : bool
            Whether verbose output is enabled or not (this is included for consistency with other methods).
        """
        # Iterates over the rows of the board and prints it legibly
        for x in range(len(board)):
            # Every 3 rows, print a blank line to separate the 3x3 subgrids
            if x % 3 == 0 and x != 0:
                print("               ")

            # Create a row as a string, adding spaces between columns and a double space after every third value
            row = [str(board[x][y]) + (' ' if y % 3 != 2 else '  ') for y in range(len(board[0]))]
            # Print the joined row
            print("".join(row))
            
   


"""
Module for the Sudoku AI in the Sudoku game.

This module provides the `SudokuAI` class, which simulates an AI player for the Sudoku game.
The AI analyzes the board, decides the next move, and checks if a move is valid.

Classes:
    SudokuAI: Simulates an AI player for the Sudoku game.

Written by: bayosoun, sodonoya and hintsimo (Komodorpudel)
"""

import time

class SudokuAI:
    """
    Simulates an AI player for the Sudoku game.

    This class provides methods to analyze the Sudoku board, make decisions based on AI intelligence, and perform moves.

    Attributes:
        game (SudokuGame): The current instance of the Sudoku game.
        board (list): The current state of the Sudoku board.
        ui (SudokuUI): User interface instance associated with the game.
        intelligence (int): AI intelligence level (0-3).

    Methods:
        __init__(self, game, intelligence): Initializes the AI with the game instance and intelligence level.
        valid_move(self, row, col, num): Validates if a move is permissible according to Sudoku rules.
        decide_move(self): Decides the next move for the AI.
        decide_move_1(self): Implements AI decision-making logic at level 1 intelligence.
        decide_move_2(self): Implements AI decision-making logic at level 2 intelligence.
        is_single_position(self, num, row, col): Checks if a number can only be placed in one position in a given row, column, or block.
        decide_move_3(self): Implements AI decision-making logic at level 3 intelligence.
    """

# -----------------------------------------------------------------
    def __init__(self, game, intelligence):
        """
        —Initializes the SudokuAI with the game instance and AI intelligence level.

        Args:
            game (SudokuGame): The current instance of the Sudoku game.
            intelligence (int): AI intelligence level (0-3).

        Attributes:
            game (SudokuGame): The game instance associated with the AI.
            board (list): The current state of the Sudoku board.
            ui (SudokuUI): User interface instance associated with the game.
            intelligence (int): AI intelligence level.
        """
        self.game = game
        self.board = None
        self.ui = game.get_ui()
        self.intelligence = intelligence # from 0 to 3

# -----------------------------------------------------------------
    def valid_move(self, row, col, num):
        """
        Validates if a move is permissible according to Sudoku rules.

        Args:
            row (int): The row index for the cell.
            col (int): The column index for the cell.
            num (int): The number intended to be placed in the cell.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if not self.board[row][col]['mutable']:
            return False
        for i in range(9):
            if self.board[row][i]['num'] == num:
                # print(f"The number {num} is already in this row.")
                return False
            if self.board[i][col]['num'] == num:
                # print(f"The number {num} is already in this column.")
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j]['num'] == num:
                    # print(f"The number {num} is already in this block.")
                    return False
        return True


# -----------------------------------------------------------------
    def decide_move(self):
        """
        Determines the next move based on the selected AI intelligence level.

        This method decides the next move to make by calling the appropriate sub-method
        (`decide_move_1`, `decide_move_2`, or `decide_move_3`) based on the AI's intelligence level.

        Returns:
            tuple: The row, column, and number to be placed as the next move, or None if no move is possible.
        """

        # *****************************************************
        def decide_move_1():
            """
            Level 1 AI Decision-Making: Basic Elimination.

            This sub-method implements the AI decision-making process at intelligence level 1.
            It uses a basic elimination strategy to find the next move by scanning for the first
            empty cell and attempting to place numbers 1 through 9. If a valid move is found, it returns the move.

            Returns:
                tuple: The row, column, and number for the next move, or None if no valid move is found.
            """

            time.sleep(1)  # Simulate think time

            # Analyze the board and return the next move as (row, col, num)
            for row in range(9):
                for col in range(9):
                    if self.board[row][col]['num'] == 0:  # Find the first empty spot
                        for num in range(1, 10):  # Try numbers 1-9
                            if self.valid_move(row, col, num):
                                return (row, col, num)
            return None

        # *****************************************************
        def decide_move_2():
            """
            Level 2 AI Decision-Making: Single Candidate.

            This sub-method implements the AI decision-making process at intelligence level 2.
            It checks each cell to determine if there's only one possible number that can be placed there,
            based on the current state of the board.

            Returns:
                tuple: The row, column, and number for the next move, or None if no valid move is found.
            """
            # +++++++++++++++++++++++++++++++++++++++++++
            def is_single_position(self, row, col, num):
                """
                Checks if a number can only be placed in one position in a row, column, or 3x3 subgrid.
                This helper method determines if a number can be uniquely placed in a specific position
                based on the Sudoku rules.
                Args:
                    num (int): The number to check.
                    row (int): The row index to check.
                    col (int): The column index to check.
                Returns:
                    bool: True if the number can only be placed in one position, False otherwise.
                """
                # Check row
                if all(self.board[row][i]['num'] != num for i in range(9) if i != col and self.board[row][i]['num'] == 0):
                    return True

                # Check column
                if all(self.board[i][col]['num'] != num for i in range(9) if i != row and self.board[i][col]['num'] == 0):
                    return True

                # Check 3x3 subgrid
                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                if all(self.board[i][j]['num'] != num for i in range(start_row, start_row + 3)
                    for j in range(start_col, start_col + 3) if (i != row or j != col) and self.board[i][j]['num'] == 0):
                    return True

                return False

            # +++++++++++++++++++++++++++++++++++++++++++

            time.sleep(1)  # Simulate think time

            for num in range(1, 10):
                for row in range(9):
                    for col in range(9):
                        if self.board[row][col]['num'] == 0 and self.valid_move(row, col, num):
                            if is_single_position(self,row, col, num):
                                return (row, col, num)

            return None


        # *****************************************************
        def decide_move_3(last_move=[None, None, None]):
            """
            Level 3 AI Decision-Making: Recursion and Backtracking.

            This sub-method implements the AI decision-making process at intelligence level 3.
            It uses a recursive backtracking algorithm to solve the Sudoku puzzle by trying
            each possible number in empty cells, backtracking if a move leads to an invalid state.

            Args:
                last_move (list): A list containing the last valid move made as [row, col, num].

            Returns:
                bool: True if the board is solved or the move is successful, False if the move leads to a dead end.
            """

            for row in range(9):
                for col in range(9):
                    if self.board[row][col]['num'] == 0:
                        for num in range(1, 10):
                            if self.valid_move(row, col, num):
                                self.board[row][col]['num'] = num
                                self.ui.display_message(f"AI placed {num} at ({row + 1}, {col + 1})")
                                self.ui.display_board_menu()
                                time.sleep(0.1)
                            
                                # Update the last valid move
                                last_move[0], last_move[1], last_move[2] = row, col, num

                                # Recursively attempt to solve the rest of the board
                                if decide_move_3(last_move):
                                    return True
                                
                                # We could not solve this entry:
                                self.ui.display_message(f"AI removed {self.board[row][col]['num']} at ({row + 1}, {col + 1})")
                                self.board[row][col]['num'] = 0
                                self.ui.display_board_menu()
                                time.sleep(0.1)
                        return False
            
            # If no empty cell is found, the board is solved
            return True
# *****************************************************

        self.board = self.game.get_board()

        if self.intelligence == 1:
            return decide_move_1()
        if self.intelligence == 2:
            return decide_move_2()
        if self.intelligence == 3:
            last_move = [None, None, None]
            decide_move_3(last_move)
            return last_move


# -----------------------------------------------------------------


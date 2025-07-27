"""
Sudoku Game Module

This module provides the `SudokuGame` class to manage the logic and state of a Sudoku game.
It handles game initialization, move validation, win condition checks, and interaction with
the user interface and AI player.

Classes:
    SudokuGame: Manages the logic and state of a Sudoku game.

Written by: bayosoun
"""

import threading
import time
from sudoku_stopwatch import SudokuStopwatch
from sudoku_highscore_manager import SudokuHighscoreManager


class SudokuGame:
    """
    A class to represent a Sudoku game.

    Attributes:
        controller : object
            The controller object managing the game flow.
        difficulty : str
            The difficulty level of the game.
        board : list of list of dict, optional
            The current state of the Sudoku board (default is None).
        user : str
            The username of the player (default is an empty string).
        mistakes : int
            The number of mistakes made by the player (default is 0).
        previous_elapsed_time : int
            The total elapsed time from previous sessions (default is 0).
        my_stopwatch : SudokuStopwatch
            An instance of the SudokuStopwatch to track time.
    """

    # -----------------------------------------------------------------
    def __init__(self, controller, difficulty, board=None, user="", mistakes=0, total_elapsed_time=0):
        """
        Initializes a new instance of the SudokuGame class.

        Parameters:
            controller: The controller object that manages game logic.
            difficulty: The difficulty level of the game.
            board (optional): The current state of the Sudoku board. Defaults to None.
            user (optional): The username of the player. Defaults to an empty string.
            mistakes (optional): The number of mistakes made by the player. Defaults to 0.
            total_elapsed_time (optional): The total elapsed time of the game in seconds. Defaults to 0.

        """
        self.controller = controller
        self.ui = controller.get_ui()
        self.ui.set_game(self)

        self.difficulty = difficulty
        self.board = board
        self.user = user
        self.mistakes = mistakes
        self.previous_elapsed_time = total_elapsed_time
        self.ai_in_use = False

        self.my_stopwatch = SudokuStopwatch()
        self.my_stopwatch.start()  # We start counting

        # Board for test purposes:
        if board is None:
            self.board = [
                [{'num': 0, 'mutable': True}, {'num': 0, 'mutable': True}, {'num': 4, 'mutable': False},
                 {'num': 6, 'mutable': False}, {'num': 7, 'mutable': False}, {'num': 8, 'mutable': False},
                 {'num': 9, 'mutable': False}, {'num': 1, 'mutable': False}, {'num': 2, 'mutable': False}],
                [{'num': 6, 'mutable': False}, {'num': 7, 'mutable': False}, {'num': 2, 'mutable': False},
                 {'num': 1, 'mutable': False}, {'num': 9, 'mutable': False}, {'num': 5, 'mutable': False},
                 {'num': 3, 'mutable': False}, {'num': 4, 'mutable': False}, {'num': 8, 'mutable': False}],
                [{'num': 1, 'mutable': False}, {'num': 9, 'mutable': False}, {'num': 8, 'mutable': False},
                 {'num': 3, 'mutable': False}, {'num': 4, 'mutable': False}, {'num': 2, 'mutable': False},
                 {'num': 5, 'mutable': False}, {'num': 6, 'mutable': False}, {'num': 7, 'mutable': False}],
                [{'num': 8, 'mutable': False}, {'num': 5, 'mutable': False}, {'num': 9, 'mutable': False},
                 {'num': 7, 'mutable': False}, {'num': 6, 'mutable': False}, {'num': 1, 'mutable': False},
                 {'num': 4, 'mutable': False}, {'num': 2, 'mutable': False}, {'num': 3, 'mutable': False}],
                [{'num': 4, 'mutable': False}, {'num': 2, 'mutable': False}, {'num': 6, 'mutable': False},
                 {'num': 8, 'mutable': False}, {'num': 5, 'mutable': False}, {'num': 3, 'mutable': False},
                 {'num': 7, 'mutable': False}, {'num': 9, 'mutable': False}, {'num': 1, 'mutable': False}],
                [{'num': 7, 'mutable': False}, {'num': 1, 'mutable': False}, {'num': 3, 'mutable': False},
                 {'num': 9, 'mutable': False}, {'num': 2, 'mutable': False}, {'num': 4, 'mutable': False},
                 {'num': 8, 'mutable': False}, {'num': 5, 'mutable': False}, {'num': 6, 'mutable': False}],
                [{'num': 9, 'mutable': False}, {'num': 6, 'mutable': False}, {'num': 1, 'mutable': False},
                 {'num': 5, 'mutable': False}, {'num': 3, 'mutable': False}, {'num': 7, 'mutable': False},
                 {'num': 2, 'mutable': False}, {'num': 8, 'mutable': False}, {'num': 4, 'mutable': False}],
                [{'num': 2, 'mutable': False}, {'num': 8, 'mutable': False}, {'num': 7, 'mutable': False},
                 {'num': 4, 'mutable': False}, {'num': 1, 'mutable': False}, {'num': 9, 'mutable': False},
                 {'num': 6, 'mutable': False}, {'num': 3, 'mutable': False}, {'num': 5, 'mutable': False}],
                [{'num': 3, 'mutable': False}, {'num': 4, 'mutable': False}, {'num': 5, 'mutable': False},
                 {'num': 2, 'mutable': False}, {'num': 8, 'mutable': False}, {'num': 6, 'mutable': False},
                 {'num': 1, 'mutable': False}, {'num': 7, 'mutable': False}, {'num': 9, 'mutable': False}]
            ]

        else:
            self.board = board


 # -----------------------------------------------------------------
    def get_difficulty(self):
        """
        Returns the difficulty level of the game.

        Examples:
            >>> from sudoku_app_controller import SudokuAppController #for doctest
            >>> from sudoku_ui_terminal import SudokuUI_Terminal # for doctest
            >>> ui = SudokuUI_Terminal()
            >>> controller = SudokuAppController(ui)
            >>> difficulty = 2
            >>> game = SudokuGame(controller, difficulty)
            >>> game.get_difficulty()
            2
        """

        return self.difficulty


 # -----------------------------------------------------------------
    def get_board(self):
        """
        Returns the current state of the Sudoku board.

        Returns:
            list: The current Sudoku board as a list of lists.
        """
        return self.board


 # -----------------------------------------------------------------
    def get_mistakes(self):
        """
        Returns the number of mistakes made by the player.

        Returns:
            int: The number of mistakes made by the player.

        Examples:
            >>> from sudoku_app_controller import SudokuAppController #for doctest
            >>> from sudoku_ui_terminal import SudokuUI_Terminal # for doctest
            >>> ui = SudokuUI_Terminal()
            >>> controller = SudokuAppController(ui)
            >>> difficulty = 2
            >>> game = SudokuGame(controller, difficulty, mistakes=2)
            >>> game.get_mistakes()
            2
        """
        return self.mistakes


 # -----------------------------------------------------------------
    def get_total_elapsed_time(self):
        """
        Returns the total elapsed time of the game.

        Returns:
            int: The total elapsed time of the game in seconds.

        Examples:
            >>> from sudoku_app_controller import SudokuAppController #for doctest
            >>> from sudoku_ui_terminal import SudokuUI_Terminal # for doctest
            >>> ui = SudokuUI_Terminal()
            >>> controller = SudokuAppController(ui)
            >>> difficulty = 2
            >>> game = SudokuGame(controller, difficulty, total_elapsed_time=20)
            >>> game.get_total_elapsed_time() >= 20
            True
        """

        return self.previous_elapsed_time + self.my_stopwatch.get_elapsed_time()


 # -----------------------------------------------------------------
    def get_user(self):
        """
        Returns the username of the player.

        Returns:
            str: The username of the player.
        """
        return self.user


 # -----------------------------------------------------------------
    def get_ui(self):
        """
        Returns the UI controller for the game.

        Returns:
            object: The UI controller object.

        """
        return self.ui


    # -----------------------------------------------------------------
    def is_valid_move(self, row, col, num):
        """
        Checks if placing a number in a specific cell is a valid move.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the move is valid, False otherwise.

        Examples:
            >>> board = [[{'num': 0, 'mutable': True} for _ in range(9)] for _ in range(9)]
            >>> from sudoku_app_controller import SudokuAppController #for doctest
            >>> from sudoku_ui_terminal import SudokuUI_Terminal # for doctest
            >>> ui = SudokuUI_Terminal()
            >>> controller = SudokuAppController(ui)
            >>> difficulty = 2
            >>> game = SudokuGame(controller, difficulty, board, total_elapsed_time=20)
            >>> game.is_valid_move(0, 0, 5)
            Move accepted.
            True
            >>> game.board[0][1]['num'] = 5
            >>> game.is_valid_move(0, 0, 5)
            The number 5 is already in this row.
            False
            >>> game.board[1][0]['num'] = 5
            >>> game.is_valid_move(0, 0, 5)
            The number 5 is already in this row.
            False
            >>> game.board[1][1]['num'] = 5
            >>> game.is_valid_move(0, 0, 5)
            The number 5 is already in this row.
            False
        """

        # We entered the same number:
        if self.board[row][col]['num'] == num:
            return True

        if not self.board[row][col]['mutable']:
            self.ui.display_message("This cell's value is given and cannot be changed.")
            return False
        
        if num == 0: # Allows to empty mutable fields.
            if not self.ai_in_use and not self.ui.get_is_graphical():
                self.ui.display_message("Move accepted.")
            return True

        for i in range(9):
            if self.board[row][i]['num'] == num:
                self.ui.display_message(f"The number {num} is already in this row.")
                self.mistakes += 1
                return False

            if self.board[i][col]['num'] == num:
                self.ui.display_message(f"The number {num} is already in this column.")
                self.mistakes += 1
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j]['num'] == num:
                    self.ui.display_message(f"The number {num} is already in this block.")
                    self.mistakes += 1
                    return False

        if not self.ai_in_use and not self.ui.get_is_graphical():
            self.ui.display_message("Move accepted.")

        return True


    # -----------------------------------------------------------------
    def check_win(self):
        """
        Checks if the current board is a winning board.

        Returns:
            bool: True if the board is a winning board, False otherwise.
        """

        full_set = set(range(1, 10))

        # Check rows and columns
        for i in range(9):
            row_set = set(cell['num'] for cell in self.board[i])
            col_set = set(self.board[j][i]['num'] for j in range(9))
            if row_set != full_set or col_set != full_set:
                return False

        # Check 3x3 squares
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                square_set = {self.board[r][c]['num'] for r in range(x, x + 3) for c in range(y, y + 3)}
                if square_set != full_set:
                    return False
        return True


    # -----------------------------------------------------------------
    def place_number(self, row, col, num):
        """
        Attempts to place a number in a specific cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to be placed in the cell.

        Returns:
            bool: True if the number was successfully placed, False otherwise.
        """

        if self.is_valid_move(row, col, num):
            self.board[row][col]['num'] = num
            # print("DEBUG: SudokuGame.place_number: Was valid and placed")
            return True
        # print("DEBUG: SudokuGame.place_number: NOT valid and NOT placed")
        return False


    # -----------------------------------------------------------------
    def play(self):
        """
        Starts the interactive play loop for the Sudoku game.

        This method manages the main game loop, where the player interacts with the game
        by making moves on the Sudoku board. It repeatedly displays the current board,
        prompts the player for their next move, validates the move, and updates the game state.
        The loop continues until the player either wins the game, makes too many mistakes, or pauses the game.

        Gameplay Logic:
        1. Displays the current game board.
        2. Prompts the player for their next move (row, column, and number).
        3. Checks if the player chose to pause the game. If so, pauses the stopwatch and opens the pause menu.
        4. Validates the move to ensure it's within the board's boundaries and adheres to Sudoku rules.
        5. Updates the board with the player's move if valid, or increments the mistake counter if invalid.
        6. Checks for win conditions or too many mistakes to determine if the game ends.
        7. Repeats the process until the game ends or is paused.

        Raises:
            ValueError: If the player's input cannot be converted to integers for row, column, or number.
        """

        while True:
            self.ui.display_board_menu()

            try:
                row, col, num = self.ui.get_next_move()
                # print("DEBUG - Inside SudokuGame.play() after asking for getting next move")
                # print(row)
                # print(col)
                # print(num)
                if row == 'pause':
                    self.my_stopwatch.pause()
                    self.controller.run_pause_menu()
                    break

                row, col = row - 1, col - 1
                # print("DEBUG - Inside SudokuGame.play()")
                # print(row)
                # print(col)
                # print(num)
                if 0 <= row < 9 and 0 <= col < 9:
                    if not self.place_number(row, col, num):
                        if self.mistakes >= 3:
                            self.lost_game_cleanup()
                            break
                    else:
                        if self.check_win():
                            self.won_game_cleanup()
                            break

                else:
                    self.ui.display_message("Please enter a valid row and column between 1 and 9.")
            except ValueError:
                self.ui.display_message("Invalid input. Please enter integers only.")

            #if self.ui.get_general_input("Type 'pause' to open pause menu or hit enter to continue: ").lower() == 'pause':
            #    self.my_stopwatch.pause()
            #    self.controller.run_pause_menu()
            #    break


 # -----------------------------------------------------------------
    def lost_game_cleanup(self):
        """
        Handles the end-of-game procedures when the player loses the game.

        This method updates the high score, pauses the stopwatch, displays a losing message,
        and then returns to the main menu.

        Example:
            Not suitable for simple doctest.
        """

        SudokuHighscoreManager.set_highscore(self.user, self.difficulty * -1)
        self.my_stopwatch.pause()
        message = (
            "!!! YOU LOSE !!!\n"
            f"Score subtracted: {self.difficulty * -1}\n"
            f"New total score: {SudokuHighscoreManager.get_user_highscore(self.user)}\n"
            "Try again, Loser!"
        )

        self.ui.display_message(message)
        self.controller.run_main_menu()


 # -----------------------------------------------------------------
    def won_game_cleanup(self):
        """
        Handles the cleanup process when the player wins the game.

        This method performs the following actions:
        - Updates the player's highscore by adding points based on the difficulty level.
        - Pauses the stopwatch.
        - Displays a message informing the player that they have won, including the score change and new total score.
        - Returns to the main menu.

        Example:
            Not suitable for simple doctest.
        """

        # print("DEBUG: Called SudokuGame.won_game_cleanup()")
        SudokuHighscoreManager.set_highscore(self.user, self.difficulty * 1)
        self.my_stopwatch.pause()
        message = (
            "!!! YOU WIN !!!\n"
            f"Score added: {self.difficulty * 1}\n"
            f"New total score: {SudokuHighscoreManager.get_user_highscore(self.user)}\n"
            "Well done!"
        )

        self.ui.display_message(message)
        self.controller.run_main_menu()


    # -----------------------------------------------------------------
    def play_with_ai(self, ai_player):
        '''
        Runs the game with an AI player making moves.

        Parameters:
        ai_player (object): The AI player object that makes decisions.

        Example:
            Not suitable for simple doctest.
        '''


        # *****************************************************
        def ai_loop():
            while not self.check_win():
                move = ai_player.decide_move()
                if move:
                    row, col, num = move
                    if self.place_number(row, col, num):

                        # Graphical:
                        if self.ui.get_is_graphical():
                            print("DEBUG: Graphical")
                            self.ui.root.after(0, self.ui.get_board_menu().display())
 
                        # Terminal:
                        else:
                            # print("DEBUG: ui is not graphical")
                            self.ui.display_message(f"AI placed {num} at ({row + 1}, {col + 1})")
                            self.ui.display_board_menu()

                    if self.check_win():
                        self.ui.display_message("AI wins!")
                        self.won_game_cleanup()
                        break
                else:
                    self.ui.display_message("AI could not make a valid move. It is time that you take over and fix this mess!\nReturning to manual input ...")
                    self.ai_in_use = False
                    time.sleep(4)
                    self.play()
                    break
        # *****************************************************

        self.ai_in_use = True
        self.ui.display_board_menu()

        if self.ui.get_is_graphical:
            ai_thread = threading.Thread(target=ai_loop)
            ai_thread.start()
        else:
            ai_loop()

# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

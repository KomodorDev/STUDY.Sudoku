"""
Module for controlling the flow of the Sudoku application.

This module provides the `SudokuAppController` class, which manages interactions
between the user interface and the game logic, handling user sessions, game states,
and navigation through different menus.

Classes:
    SudokuAppController

Written by: hintsimo (Komodorpudel)
"""

import os
import sys
from sudoku_board_generator import SudokuBoardGenerator
from sudoku_save_load_manager import SudokuSaveLoadManager
from sudoku_game import SudokuGame
from sudoku_ai import SudokuAI

from sudoku_ui_terminal import SudokuUI_Terminal # for doctests

class SudokuAppController:
    """
    Controller class for managing the flow of the Sudoku application.

    This class handles interactions between the user interface and the game logic,
    managing user sessions, game states, and navigation through different menus.
    """

# -----------------------------------------------------------------
    def __init__(self, ui):
        """
        Initialize the SudokuAppController with the provided user interface.

        Parameters:
        ui (UI): The user interface instance for the application.

        Example:
        >>> ui = SudokuUI_Terminal()
        >>> app = SudokuAppController(ui)
        >>> app.ui == ui
        True
        >>> app.game is None
        True
        >>> app.user is None
        True
        >>> app.user_save_path is None
        True
        """

        self.ui = ui
        self.game = None  # This will be a GameLogic instance, given by game when we start game
        self.user = None
        self.user_save_path = None


# -----------------------------------------------------------------
    def get_ui(self):
        """
        Retrieve the user interface instance.

        Returns:
        ui: The user interface instance.

        Example:
        >>> ui = SudokuUI_Terminal()
        >>> app = SudokuAppController(ui)
        >>> app.get_ui() is ui
        True
        """

        return self.ui


# -----------------------------------------------------------------
    def get_user(self):
        """
        Retrieve the current user.

        Returns:
        user: The current user instance.

        Example:
        >>> ui = SudokuUI_Terminal()
        >>> app = SudokuAppController(ui)
        >>> app.get_user() is None
        True
        """

        return self.user


# -----------------------------------------------------------------
    def run_welcome_menu(self):
        """
        Display the welcome menu and initialize the user session.

        This method prompts the user to select or create a user profile, and then
        navigates to the main menu.

        Example:
        Not suitable for simple doctest
        """

        self.user = self.ui.display_welcome_menu() # We get user object from UI

        # Create save_path directly if not existing:
        if not os.path.exists(SudokuSaveLoadManager.get_user_path(self.user)):
            self.user_save_path = SudokuSaveLoadManager.set_user_path(self.user)

        else:
            self.user_save_path = SudokuSaveLoadManager.get_user_path(self.user)

        self.run_main_menu()


# -----------------------------------------------------------------
    def run_main_menu(self):
        """
        Calls the ui to display the main menu and handle user choices.

        This method provides options for starting a new game, starting a new game with AI,
        loading an existing game, viewing the highscore, or exiting the application.

        Example:
        Not suitable for simple doctest
        """

        while True:
            choice = self.ui.display_main_menu()

            if choice == '1':
                self.run_new_game_menu()
                break
            elif choice == '2':
                self.run_new_game_with_ai_menu()
                break
            elif choice == '3':
                self.run_load_game_menu()
                break
            elif choice == '4':
                self.run_highscore_menu()
                break
            elif choice == '5':
                self.ui.display_message("Exiting the game. Goodbye!")
                sys.exit(0)
            else:
                # Not really relevant for GUI since we can limit input options
                self.ui.display_message("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


# -----------------------------------------------------------------
    def run_new_game_menu(self):
        """
        Calls ui to ask for user input (difficulty) and start a new game with the selected difficulty.

        This method prompts the user to enter a difficulty level and then starts a new game
        with a generated Sudoku board.

        Example:
        Not suitable for simple doctest
        """

        while True:
            try:
                difficulty = self.ui.get_general_input("Enter difficulty (0-9) (be warned: Higher difficulty leads to longer calculation times): ")
                if difficulty is None:
                    self.run_main_menu()
                else:
                    difficulty = int(difficulty)
                if 0 <= difficulty <= 9:
                    break
                else:
                    self.ui.display_message("Please enter a valid difficulty between 0 and 9.")
            except ValueError:
                self.ui.display_message("Invalid input. Please enter an integer between 0 and 9.")

        generated_board = SudokuBoardGenerator.generate_board(difficulty)
        #generated_board = None
        self.game = SudokuGame(self, difficulty, generated_board, self.user)
        self.game.play()


# -----------------------------------------------------------------
    def run_pause_menu(self):
        """
        Calls ui to display the pause menu and handle user choices.

        This method provides options to resume the game, save the current game, or return
        to the main menu.
    
        Example:
        Not suitable for simple doctest
        """

        while True:
            choice = self.ui.display_pause_menu()
            if choice == '1':
                self.ui.display_message("Resuming game...")
                self.game.play()
                break

            elif choice == '2':
                ####################
                game_name = SudokuSaveLoadManager.save_game(self.game)
                self.get_ui().display_message(f"Game saved as {game_name}.")

            elif choice == '3':
                self.ui.display_message("Returning to main menu...")
                self.run_main_menu()
                break

            else:
                self.ui.display_message("Invalid choice. Please enter 1, 2, or 3.")


# -----------------------------------------------------------------
    def run_new_game_with_ai_menu(self):
        """
        Display the new game with AI menu and start a new game for the AI to solve.

        This method prompts the user to enter a difficulty level for the board that the AI
        should solve and then starts a new game with a generated Sudoku board.
    
        Example:
        Not suitable for simple doctest
        """

        while True:
            try:
                difficulty = int(self.ui.get_general_input("Enter difficulty of board that AI should solve (0-9): "))
                if 0 <= difficulty <= 9:
                    intelligence = int(self.ui.get_general_input("Enter intelligence of AI (1-3): "))
                    if 1 <= intelligence <= 3:
                        break
                    else:
                        self.ui.display_message("Please enter a valid intelligence between 0 and 3.")
                else:
                    self.ui.display_message("Please enter a valid difficulty between 0 and 9.")
            except ValueError:
                self.ui.display_message("Invalid input. Please enter an integer between 0 and 9.")
        generated_board = SudokuBoardGenerator.generate_board(difficulty)
        my_game = SudokuGame(self, difficulty, generated_board, self.user)
        my_ai = SudokuAI(my_game, intelligence)
        my_game.play_with_ai(my_ai)


# -----------------------------------------------------------------
    def run_load_game_menu(self):
        """
        Calls ui to display the load game menu and load a selected saved game.

        This method allows the user to choose a saved game to load and then resumes
        the game from the saved state.

        Example:
        Not suitable for simple doctest
        """

        # print(f"DEBUG: Available saved games: {games}")  # Debug print

        game_choice = self.ui.display_load_menu()
        if game_choice.lower() == 'return':
            self.run_main_menu()
        else:
            game_path = os.path.join(self.user_save_path, game_choice)
            self.game = SudokuSaveLoadManager.load_game(game_path, self)
            self.game.play()


# -----------------------------------------------------------------
    def run_highscore_menu(self):
        """
        Calls ui to display the highscore menu.

        This method shows the highscore list and allows the user to return to the main menu.
        
        Example:
        Not suitable for simple doctest
        """

        choice = self.ui.display_highscore_menu()
        if choice == 'return':
            self.run_main_menu()


# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

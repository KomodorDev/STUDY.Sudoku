"""
Module for defining the abstract base class for the Sudoku UI.

Classes:
    SudokuUI: Abstract base class for the Sudoku UI.

Example usage:
    This class is meant to be subclassed by concrete UI implementations such as `SudokuUI_Terminal`
    and `SudokuUI_Graphical`. Subclasses should provide implementations for all abstract methods.

Written by: hintsimo (Komodorpudel)
"""

from abc import ABC, abstractmethod

class SudokuUI(ABC):
    """
    Abstract base class for the Sudoku UI.

    This class defines the interface for various UI implementations of the Sudoku game.
    It includes methods for setting up the game, displaying various menus, displaying the game board,
    and handling user input.

    The following classes inherit from it:
    - SudokuUI_Terminal
    - SudokuUI_Graphical

    """
    @abstractmethod
    def __init__(self, game=None, user=None):
        """Initialisation"""

    @abstractmethod
    def set_game(self, game):
        """set_game for UI"""

    @abstractmethod
    def display_welcome_menu(self):
        """Display a welcome screen for user authentication."""


    @abstractmethod
    def display_main_menu(self):
        """Display the main menu options to the user."""


    @abstractmethod
    def display_board_menu(self):
        """Display the game board."""


    @abstractmethod
    def display_pause_menu(self):
        """Display pause menu options."""


    @abstractmethod
    def display_load_menu(self):
        """Display a menu to load a saved game."""


    @abstractmethod
    def display_highscore_menu(self):
        """Display highscores."""


    @abstractmethod
    def display_message(self, message):
        """Display a message to the user."""


    @abstractmethod
    def get_general_input(self, prompt: str) -> str:
        """Display a prompt and return the user's input as a string."""


    @abstractmethod
    def get_next_move(self):
        """Prompt the user to enter their move."""

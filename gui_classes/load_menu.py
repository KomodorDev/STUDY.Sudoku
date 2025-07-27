"""
Module for displaying and interacting with the saved games menu in the GUI.

This module provides the `LoadMenu` class, which creates and manages the display
of the saved games menu, allowing users to select and load previously saved games.

Classes:
    LoadMenu: Manages the display and interaction with the saved games menu.

Written by: hintsimo (Komodorpudel) and sodonoya
"""

import tkinter as tk
from sudoku_save_load_manager import SudokuSaveLoadManager  # Assume this module provides the saved games

class LoadMenu:
    """
    Class for managing the display and interaction with the saved games menu.

    This class creates the UI elements for the saved games menu, handles user input
    for selecting a saved game, and provides a back button functionality.

    Attributes:
        ui (UI): The user interface instance.
        done (tk.BooleanVar): Condition variable to signal completion.
        user (SudokuUser): The current user instance.
        symbol_label (tk.Label): Label to display the changing symbol.
        symbol_state (bool): State of the changing symbol.
    """

# -----------------------------------------------------------------
    def __init__(self, ui):
        """
        Initialize the LoadMenu with the given user interface.

        Parameters:
            ui (UI): The user interface instance.
        """

        print("DEBUG: Called SavedGamesMenu __init__")
        self.ui = ui
        self.done = tk.BooleanVar(value=False)  # Condition variable to signal completion
        self.user = self.ui.get_user()

        self.symbol_label = None
        self.symbol_state = True


# -----------------------------------------------------------------
    def display(self):
        """
        Display the saved games menu.

        This method clears the current window content and creates the UI elements
        for the saved games menu, including buttons for each saved game and a back button.

        Example:
            Not suitable for simple doctest.
        """

        print("DEBUG: Called SavedGamesMenu.display()")
        # Clear the current window content
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        print("DEBUG: Displaying Saved Games Menu")

        # Create saved games menu content
        label = tk.Label(self.ui.root, text="Saved Games:", font=("Arial", 24))
        label.pack(pady=20)
        print("DEBUG: Created and packed label")

        saved_games = SudokuSaveLoadManager.get_list_of_saved_games(self.user)  # Assume this method returns a list of saved games

        # Create saved games overview
        for game in saved_games:
            game_button = tk.Button(self.ui.root, text=game, font=("Arial", 14), command=lambda g=game: self.ui.set_return_value(g))
            game_button.pack(pady=5)
            print(f"DEBUG: Created and packed button for saved game {game}")

        # Back button
        back_button = tk.Button(self.ui.root, text="Back", command=lambda: self.ui.set_return_value('return'))
        back_button.pack(pady=10)
        print("DEBUG: Created and packed Back button")

        # Symbol changing label
        self.symbol_label = tk.Label(self.ui.root, text="/", font=("Arial", 24))
        self.symbol_label.pack(pady=20)
        print("DEBUG: Created and packed symbol changing label")
        self.change_symbol()
        print("DEBUG: Change symbol started")


# -----------------------------------------------------------------
    def change_symbol(self):
        """
        Change the symbol displayed in the symbol label.

        This method alternates the symbol in the symbol label between '/' and '\'
        every second.

        Example:
            Not suitable for simple doctest.
        """

        if self.symbol_label.winfo_exists():
            if self.symbol_state:
                self.symbol_label.config(text="/")
            else:
                self.symbol_label.config(text="\\")
            self.symbol_state = not self.symbol_state
            self.ui.root.after(1000, self.change_symbol)


# -----------------------------------------------------------------

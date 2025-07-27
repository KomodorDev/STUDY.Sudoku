"""
Highscore Menu for Sudoku Game

This module defines the `HighscoreMenu` class, which represents a graphical interface 
for displaying the highscores of the Sudoku game. It interacts with the user interface 
manager and the highscore manager to display and manage highscores.

Classes:
    HighscoreMenu: A class to display and manage the Sudoku game highscores in a graphical window.

Written by: sodonoya
"""

import tkinter as tk
from sudoku_highscore_manager import SudokuHighscoreManager

class HighscoreMenu:
    """
    Represents a graphical highscore menu for displaying Sudoku game highscores.

    Attributes:
        ui (UIManager): The user interface manager that controls the UI elements.
        done (tk.BooleanVar): Condition variable to signal completion state.
        user (str): The current user of the highscore menu.
        symbol_label (tk.Label or None): Label for displaying changing symbols.
        symbol_state (bool): State flag for symbol toggling.

    Methods:
        __init__(self, ui):
            Initializes the HighscoreMenu instance.

        display(self):
            Clears the current window content and displays highscores and a back button.

        change_symbol(self):
            Changes the symbol on `symbol_label` periodically.
    """


# -----------------------------------------------------------------
    def __init__(self, ui):
        """
        Initializes the HighscoreMenu instance.

        Args:
            ui (UIManager): The user interface manager instance.
        """
        print("DEBUG: Called HighscoreMenu __init__")
        self.ui = ui
        self.done = tk.BooleanVar(value=False)  # Condition variable to signal completion
        self.user = self.ui.get_user()

        self.symbol_label = None
        self.symbol_state = True


# -----------------------------------------------------------------
    def display(self):
        """
        Clears the current window content and displays highscores and a back button.
        """
        print("DEBUG: Called HighscoreMenu.display()")
        # Clear the current window content
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        print("DEBUG: Displaying Highscore Menu")

        # Create welcome menu content
        label = tk.Label(self.ui.root, text="Highscores:", font=("Arial", 24))
        label.pack(pady=20)
        print("DEBUG: Created and packed label")

        highscores = SudokuHighscoreManager.get_highscores()

        # Create Highscores overview
        for username, score in highscores:
            highscore_label = tk.Label(self.ui.root, text=f"{username}: {score}", font=("Arial", 14))
            highscore_label.pack(pady=5)
            print(f"DEBUG: Created and packed highscore label for {username} with score {score}")

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
        Changes the symbol on `symbol_label` periodically.
        """
        if self.symbol_label.winfo_exists():
            if self.symbol_state:
                self.symbol_label.config(text="/")
            else:
                self.symbol_label.config(text="\\")
            self.symbol_state = not self.symbol_state
            self.ui.root.after(1000, self.change_symbol)


# -----------------------------------------------------------------

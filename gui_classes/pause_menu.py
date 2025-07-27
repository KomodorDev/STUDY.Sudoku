"""
Module for displaying and interacting with the pause menu in the GUI.

This module provides the `PauseMenu` class, which creates and manages the display
of the pause menu, allowing users to continue the game, save the current game, or
return to the main menu.

Classes:
    PauseMenu: Manages the display and interaction with the pause menu.

Written by: hintsimo (Komodorpudel)
"""

import tkinter as tk

class PauseMenu:
    """
    Class for managing the display and interaction with the pause menu.

    This class creates the UI elements for the pause menu, handles user input
    for continuing the game, saving the current game, or returning to the main menu,
    and provides a changing symbol animation.

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
        Initialize the PauseMenu with the given user interface.

        Parameters:
            ui (UI): The user interface instance.
        """

        print("DEBUG: Called MainMenu __init__")
        self.ui = ui
        self.done = tk.BooleanVar(value=False)  # Condition variable to signal completion
        self.user = self.ui.get_user()

        self.symbol_label = None
        self.symbol_state = True


# -----------------------------------------------------------------
    def display(self):
        """
        Display the pause menu.

        This method clears the current window content and creates the UI elements
        for the pause menu, including buttons for continuing the game, saving the
        current game, and returning to the main menu.

        Example:
            Not suitable for simple doctest.
        """

        print("DEBUG: Called PauseMenu.display()")
        # Clear the current window content
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        # Create pause menu content
        label = tk.Label(self.ui.root, text="Pause Menu", font=("Arial", 24))
        label.pack(pady=20)
        print("DEBUG: Created and packed label")

        # Define button width
        button_width = 40

        # Menu buttons
        btn1 = tk.Button(self.ui.root, text="Continue", width=button_width, command=lambda: self.ui.set_return_value('1'))
        btn1.pack(pady=10)
        print("DEBUG: Created and packed 'Continue' button")

        btn2 = tk.Button(self.ui.root, text="Save current game", width=button_width, command=lambda: self.ui.set_return_value('2'))
        btn2.pack(pady=10)
        print("DEBUG: Created and packed 'Save current game' button")

        btn3 = tk.Button(self.ui.root, text="Return to main menu", width=button_width, command=lambda: self.ui.set_return_value('3'))
        btn3.pack(pady=10)
        print("DEBUG: Created and packed 'Return to main menu' button")

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

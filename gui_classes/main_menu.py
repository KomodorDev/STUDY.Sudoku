"""
Module for displaying and interacting with the main menu in the GUI.

This module provides the `MainMenu` class, which creates and manages the display
of the main menu, allowing users to start a new game, start a game with AI, load
an unfinished game, view the highscore, or exit the application.

Classes:
    MainMenu: Manages the display and interaction with the main menu.

Written by: hintsimo (Komodorpudel) and sodonoya
"""

import tkinter as tk

class MainMenu:
    """
    Class for managing the display and interaction with the main menu.

    This class creates the UI elements for the main menu, handles user input
    for selecting various options, and provides a changing symbol animation.

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
        Initialize the MainMenu with the given user interface.

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
        Display the main menu.

        This method clears the current window content and creates the UI elements
        for the main menu, including buttons for starting a new game, starting a
        game with AI, loading an unfinished game, viewing the highscore, and exiting
        the application.

        Example:
            Not suitable for simple doctest.
        """

        print("DEBUG: Called MainMenu.display()")
        # Clear the current window content
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        # Create Main menu content
        label = tk.Label(self.ui.root, text=f"Main Menu (User: {self.user.get_username()})", font=("Arial", 24))
        label.pack(pady=20)
        print("DEBUG: Created and packed label")

        # Define button width
        button_width = 40

        # Menu buttons
        btn1 = tk.Button(self.ui.root, text="Start new game", width=button_width, command=lambda: self.ui.set_return_value('1'))
        btn1.pack(pady=10)
        print("DEBUG: Created and packed 'Start new game' button")

        btn2 = tk.Button(self.ui.root, text="Start game with AI player (not implemented in GUI)", width=button_width, state=tk.DISABLED)
        btn2.pack(pady=10)
        print("DEBUG: Created and packed 'Start game with AI player' button")

        btn3 = tk.Button(self.ui.root, text="Load unfinished game", width=button_width, command=lambda: self.ui.set_return_value('3'))
        btn3.pack(pady=10)
        print("DEBUG: Created and packed 'Load unfinished game' button")

        btn4 = tk.Button(self.ui.root, text="Highscore", width=button_width, command=lambda: self.ui.set_return_value('4'))
        btn4.pack(pady=10)
        print("DEBUG: Created and packed 'Highscore' button")

        btn5 = tk.Button(self.ui.root, text="Exit", width=button_width, command=lambda: self.ui.root.destroy())
        btn5.pack(pady=10)
        print("DEBUG: Created and packed 'Exit' button")

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

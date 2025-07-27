"""
Graphical User Interface for Sudoku

This module provides a graphical user interface (GUI) for the Sudoku game. It uses the tkinter library
to create various menu screens and manage user interactions in a windowed environment.

Classes:
    SudokuUI_Graphical: A class to manage the graphical UI for the Sudoku game.

Written by: sodonoya and hintsimo (Komodorpudel)
"""
import tkinter as tk
from tkinter import simpledialog
from sudoku_ui import SudokuUI

from gui_classes.welcome_menu import WelcomeMenu
from gui_classes.main_menu import MainMenu
from gui_classes.board_menu import BoardMenu
from gui_classes.pause_menu import PauseMenu
from gui_classes.load_menu import LoadMenu
from gui_classes.highscore_menu import HighscoreMenu

class SudokuUI_Graphical(SudokuUI):
    """
    Manages the graphical user interface for the Sudoku game.

    Attributes:
        game (SudokuGame): The current Sudoku game instance.
        user (SudokuUser): The current user instance.
        current_menu (object): The currently active menu.
        return_value (any): The return value from the current menu.
        root (tk.Tk): The main window for the GUI.
        icon (tk.PhotoImage): The icon for the application window.
        is_graphical (bool): Indicates if the UI is graphical.
        board_menu (BoardMenu): The board menu instance.
        highscore_menu (HighscoreMenu): The highscore menu instance.
        load_menu (LoadMenu): The load menu instance.
        main_menu (MainMenu): The main menu instance.
        pause_menu (PauseMenu): The pause menu instance.
        welcome_menu (WelcomeMenu): The welcome menu instance.

    Methods:
        __init__(self, game=None, user=None): Initializes the graphical UI.
        set_game(self, game): Sets the current game.
        get_game(self): Retrieves the current game.
        set_user(self, user): Sets the current user.
        get_user(self): Retrieves the current user.
        get_board_menu(self): Retrieves the board menu instance.
        get_is_graphical(self): Returns whether the UI is graphical.
        set_return_value(self, return_value): Sets the return value and signals completion.
        display_welcome_menu(self): Displays the welcome menu.
        display_main_menu(self): Displays the main menu.
        display_board_menu(self): Displays the Sudoku board.
        display_pause_menu(self): Displays the pause menu.
        display_load_menu(self): Displays the load game menu.
        display_highscore_menu(self): Displays the highscore menu.
        get_general_input(self, prompt): Prompts the user for general input.
        get_next_move(self): Retrieves the next move from the user.
        display_message(self, message): Displays a message to the user.
    """

# -----------------------------------------------------------------
    def __init__(self, game=None, user=None):
        """
        Initializes the graphical UI.

        Parameters:
            game (SudokuGame, optional): The current Sudoku game instance. Defaults to None.
            user (SudokuUser, optional): The current user instance. Defaults to None.
        """
        self.game = game
        self.user = user
        self.is_graphical = True

        self.current_menu = None
        self.board_menu = None
        self.highscore_menu = None
        self.load_menu = None
        self.main_menu = None
        self.pause_menu = None
        self.welcome_menu = None
        self.return_value = None

        # Here we setup the main paramenters for the menu:
        self.root = tk.Tk()
        self.root.title("Sudoku Game (by Simon, Soundi, and Yannick)")
        self.root.geometry("800x800")  # Set the window size

        self.icon = tk.PhotoImage(file="sudoku.png")
        self.root.iconphoto(False, self.icon)


# -----------------------------------------------------------------
    def set_game(self, game):
        """
        Sets the current game.

        Parameters:
            game (SudokuGame): The current Sudoku game instance.
        """

        self.game = game

# -----------------------------------------------------------------
    def get_game(self):
        """
        Retrieves the current game.

        Returns:
            SudokuGame: The current Sudoku game instance.
        """
        return self.game


# -----------------------------------------------------------------
    def set_user(self, user):
        """
        Sets the current user.

        Parameters:
            user (SudokuUser): The current user instance.
        """

        self.user = user


# -----------------------------------------------------------------
    def get_user(self):
        """
        Retrieves the current user.

        Returns:
            SudokuUser: The current user instance.
        """

        return self.user


# -----------------------------------------------------------------
    def get_board_menu(self):
        """
        Retrieves the board_memu

        Returns:
            BoardMenu: The current BoardMenu instance
        """

        return self.board_menu

# -----------------------------------------------------------------
    def get_is_graphical(self):
        """
        Return info if ui is graphical
        """
        return self.is_graphical

# -----------------------------------------------------------------
    def set_return_value(self, return_value):
        """
        Sets the return value and signals completion.

        Parameters:
            return_value (any): The return value from the current menu.
        """

        self.return_value = return_value
        self.current_menu.done.set(True)


# -----------------------------------------------------------------
    def display_welcome_menu(self):
        """
        Displays the welcome menu and waits for user interaction.

        Returns:
            SudokuUser: The current user after login or account creation.
        """
        if self.welcome_menu is None:
            self.welcome_menu = WelcomeMenu(self)
        #print("DEBUG: Called display_welcome_menu")
        self.current_menu = self.welcome_menu
        self.welcome_menu.display()
        self.root.wait_variable(self.current_menu.done)

        self.user = self.return_value
        #print("DEBUG: Exiting display_welcome_menu()")
        return self.return_value


# -----------------------------------------------------------------
    def display_main_menu(self):
        """
        Displays the main menu and waits for user interaction.

        Returns:
            str: User's choice from the main menu.
        """
        if self.main_menu is None:
            self.main_menu = MainMenu(self)

        #print("DEBUG: Called display_main_menu")
        self.current_menu = self.main_menu
        self.main_menu.display()
        self.root.wait_variable(self.current_menu.done)

        #print(f"DEBUG: SudokuUI_Graphical.display_main_menu() - self.return_value: {self.return_value}")
        return self.return_value


# -----------------------------------------------------------------
    def display_board_menu(self):
        """
        Displays the Sudoku board and waits for user interaction.
        """
        if self.board_menu is None:
            self.board_menu = BoardMenu(self)

        self.current_menu = self.board_menu
        self.board_menu.display()
        self.root.wait_variable(self.current_menu.done)

        #print(f"DEBUG: SudokuUI_Graphical.display_board() - self.return_value: {self.return_value}")
        # does not return anything


# -----------------------------------------------------------------
    def display_pause_menu(self):
        """
        Displays the pause menu and waits for user interaction.

        Returns:
            str: User's choice from the pause menu.
        """
        if self.pause_menu is None:
            self.pause_menu = PauseMenu(self)
        #print("DEBUG: Called display_pause_game()")

        self.current_menu = self.pause_menu
        self.pause_menu.display()
        self.root.wait_variable(self.current_menu.done)

        #print(f"DEBUG: SudokuUI_Graphical.display_load_menu() - self.return_value: {self.return_value}")
        return self.return_value


# -----------------------------------------------------------------
    def display_load_menu(self):
        """
        Displays the load game menu and waits for user interaction.

        Returns:
            str: The selected saved game or 'return' to return to the main menu.
        """
        if self.load_menu is None:
            self.load_menu = LoadMenu(self)

        #print("DEBUG: Called display_load_game()")
        self.current_menu = self.load_menu
        self.current_menu.display()
        self.root.wait_variable(self.current_menu.done)

        #print(f"DEBUG: SudokuUI_Graphical.display_load_menu() - self.return_value: {self.return_value}")
        return self.return_value


# -----------------------------------------------------------------
    def display_highscore_menu(self):
        """
        Displays the highscore menu and waits for user interaction.

        Returns:
            str: User's choice to return to the main menu.
        """
        if self.highscore_menu is None:
            self.highscore_menu = HighscoreMenu(self)

        self.current_menu = self.highscore_menu
        self.current_menu.display()
        self.root.wait_variable(self.current_menu.done)

        #print(f"DEBUG: SudokuUI_Graphical.display_highscore_menu() - self.return_value: {self.return_value}")
        return self.return_value


# -----------------------------------------------------------------
    def get_general_input(self, prompt):
        """
        Prompts the user for general input.

        Parameters:
            prompt (str): The prompt message for the input.

        Returns:
            str: The user's input.
        """

        return simpledialog.askstring("Input", prompt, parent=self.root)


# -----------------------------------------------------------------
    def get_next_move(self):
        """
        Retrieves the next move from the user.

        Returns:
            tuple: The row, column, and number for the next move.
        """

        return self.return_value[0], self.return_value[1], self.return_value[2],


# -----------------------------------------------------------------
    def display_message(self, message):
        """
        Displays a message to the user.

        Parameters:
            message (str): The message to be displayed.
        """

        message_window = tk.Toplevel()
        message_window.title("Message")

        # Create a label to display the message
        message_label = tk.Label(message_window, text=message, font=("Arial", 14), padx=10, pady=10)
        message_label.pack()

        # Create an OK button to close the message window
        ok_button = tk.Button(message_window, text="OK", command=message_window.destroy)
        ok_button.pack(pady=5)

        # Center the message window
        message_window.geometry("300x100")
        message_window.transient()  # Keep it on top of the main window
        message_window.grab_set()  # Make the message window modal
        message_window.wait_window()  # Wait until the message window is closed


# -----------------------------------------------------------------

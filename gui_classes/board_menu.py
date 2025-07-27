"""
Module for displaying and interacting with the Sudoku board in the GUI.

This module provides the `Board` class, which creates and manages the display
of the Sudoku board, handles user input for entering numbers, and provides
a pause functionality.

Classes:
    Board: Manages the display and interaction with the Sudoku board.

Written by: hintsimo (Komodorpudel) and sodonoya
"""

import tkinter as tk
import datetime

class BoardMenu:
    """
    Class for managing the display and interaction with the Sudoku board.

    This class creates the UI elements for the Sudoku board, handles user input
    for entering numbers, tracks mistakes and elapsed time, and provides a
    pause functionality.

    Attributes:
        ui (UI): The user interface instance.
        done (tk.BooleanVar): Condition variable to signal completion.
        user (SudokuUser): The current user instance.
        game (SudokuGame): The current game instance.
        board (list): The current state of the Sudoku board.
        mistakes_label (tk.Label): Label to display the number of mistakes.
        time_label (tk.Label): Label to display the elapsed time.
        changes (list): List to store the changes (row, col, num).
        symbol_label (tk.Label): Label to display the changing symbol.
        symbol_state (bool): State of the changing symbol.
    """


# -----------------------------------------------------------------
    def __init__(self, ui):
        """
        Initialize the Board with the given user interface.

        Parameters:
            ui (UI): The user interface instance.
        """
        #print("DEBUG: Called Board __init__")
        self.ui = ui
        self.done = tk.BooleanVar(value=False)  # Condition variable to signal completion
        self.user = self.ui.get_user()
        self.game = self.ui.get_game()
        self.board = self.game.get_board()

        self.mistakes_label = None
        self.time_label = None
        self.changes = []  # List to store the changes (row, col, num)

        self.symbol_label = None
        self.symbol_state = True


# -----------------------------------------------------------------
    def display(self):
        """
        Display the Sudoku board.

        This method clears the current window content and creates the UI elements
        for the Sudoku board, including entries for mutable cells and labels for
        non-mutable cells. It also displays the number of mistakes, elapsed time,
        and provides a pause button.

        Example:
            Not suitable for simple doctest.
        """

        # Clear the current window content
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        # Create board menu content
        label = tk.Label(self.ui.root,
                         text=f"{self.user.get_username()}'s current game | Difficulty: {self.game.get_difficulty()} / 9",
                         font=("Arial", 24), fg="#00A660")
        label.pack(pady=20)

        # Create the Sudoku board grid
        board_frame = tk.Frame(self.ui.root)
        board_frame.pack(pady=20)

        canvas = tk.Canvas(board_frame, width=450, height=450)
        canvas.pack()

        # Draw the grid lines
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            canvas.create_line(50 * i, 0, 50 * i, 450, width=line_width)
            canvas.create_line(0, 50 * i, 450, 50 * i, width=line_width)

        # Draw the grid lines with thicker lines around the 3x3 boxes
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            canvas.create_line(50 * i, 0, 50 * i, 450, width=line_width)
            canvas.create_line(0, 50 * i, 450, 50 * i, width=line_width)

        # Place the numbers and entry boxes on the grid
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                x1, y1 = 50 * j, 50 * i
                x2, y2 = 50 * (j + 1), 50 * (i + 1)

                if cell['mutable']:
                    # Create an Entry widget slightly smaller than the cell
                    entry = tk.Entry(board_frame, width=2, font=("Arial", 18), justify='center', fg='#814F66', bd=0)
                    entry.insert(0, str(cell['num']) if cell['num'] != 0 else '')
                    entry.bind("<Return>",
                            lambda e, x=i + 1, y=j + 1, entry=entry: self.store_change_and_exit(x, y, entry))

                    # Place the entry widget within the cell, with some padding
                    entry_window = canvas.create_window((x1 + x2) // 2, (y1 + y2) // 2, window=entry, width=46, height=46)
                else:
                    # Draw the number directly on the canvas
                    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(cell['num']), font=("Arial", 18), fill='#80A8E7')

        # Guide
        label = tk.Label(self.ui.root, text="Press 'enter' to confirm your input!", fg="#00A660")
        label.pack(pady=20)

        # Display mistakes
        self.mistakes_label = tk.Label(self.ui.root, text=f"Mistakes: {self.game.get_mistakes()} / 3",
                                       font=("Arial", 14), fg="#00A660")
        self.mistakes_label.pack(pady=10)

        # Display elapsed time
        self.time_label = tk.Label(self.ui.root, text=self.get_elapsed_time(), font=("Arial", 14), fg="#00A660")
        self.time_label.pack(pady=10)
        self.update_time()

        # Pause button
        pause_button = tk.Button(self.ui.root, text="Pause", command=lambda: self.open_pause_menu(), fg="#00A660")
        pause_button.pack(pady=10)

        # Symbol changing label
        self.symbol_label = tk.Label(self.ui.root, text="/", font=("Arial", 24), fg="#00A660")
        self.symbol_label.pack(pady=20)
        self.change_symbol()


# -----------------------------------------------------------------
    def store_change_and_exit(self, i, j, entry):
        """
        Store the change made to the Sudoku board and signal completion.

        This method stores the new value entered by the user in the Sudoku board
        and signals that the user has made a change.

        Parameters:
            i (int): The row index of the cell.
            j (int): The column index of the cell.
            entry (tk.Entry): The entry widget containing the new value.

        Example:
            Not suitable for simple doctest.
        """
        try:
            new_value = int(entry.get())
            if 0 <= new_value <= 9:
                self.changes.append((i, j, new_value))
                print(f"DEBUG: Stored change at ({i}, {j}) with new value {new_value}")
            else:
                entry.delete(0, tk.END)
                entry.insert(0, '')
                print(f"DEBUG: Invalid value {new_value} entered at ({i}, {j})")
        except ValueError:
            entry.delete(0, tk.END)
            entry.insert(0, '')
            print(f"DEBUG: Non-integer value entered at ({i}, {j})")

        # Print out the changes list
        print("DEBUG: Board - Current changes list:", self.changes)
        if self.changes:
            self.ui.set_return_value(self.changes[-1])  # This sets return_value to the most recent change


# -----------------------------------------------------------------
    def open_pause_menu(self):
        """
        Open the pause menu and signal completion.

        This method appends a pause signal to the changes list and signals that
        the user has opened the pause menu.

        Example:
            Not suitable for simple doctest.
        """
        self.changes.append(('pause', None, None))

        if self.changes:
            self.ui.set_return_value(self.changes[-1])  # This sets return_value to the most recent change
        self.done.set(True)


# -----------------------------------------------------------------
    def update_time(self):
        """
        Update the elapsed time display.

        This method updates the elapsed time label every second.

        Example:
            Not suitable for simple doctest.
        """
        if self.time_label and self.time_label.winfo_exists():
            self.time_label.config(text=self.get_elapsed_time())
        self.ui.root.after(1000, self.update_time)


# -----------------------------------------------------------------
    def get_elapsed_time(self):
        """
        Get the formatted elapsed time.

        This method returns the formatted elapsed time of the game.

        Returns:
            str: The formatted elapsed time.

        Example:
            Not suitable for simple doctest.
        """
        elapsed_time = self.game.get_total_elapsed_time()
        formatted_time = str(datetime.timedelta(seconds=elapsed_time))
        return f"Time elapsed: {formatted_time}"


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

"""
Module for the Welcome Menu in the Sudoku application.

This module provides the `WelcomeMenu` class, which creates and manages the welcome screen
for user authentication in the Sudoku game. It handles user signup and login, and displays
various elements of the welcome menu.

Classes:
    WelcomeMenu: Manages the welcome screen for user authentication.

Written by: hintsimo (Komodorpudel)
"""

import tkinter as tk
from sudoku_user import SudokuUser

class WelcomeMenu:
    """
    Class for managing the welcome screen for user authentication in the Sudoku game.

    This class creates the UI elements for the welcome screen, handles user input for
    username and password, and manages the signup and login process.

    Attributes:
        ui (UI): The user interface instance.
        done (tk.BooleanVar): Condition variable to signal completion.
        user (SudokuUser): The current user instance.

        username_entry (tk.Entry): Entry widget for the username.
        username_exists_label (tk.Label): Label indicating if the username exists.
        username_exists (bool): Flag to check if the username exists.

        password_entry (tk.Entry): Entry widget for the password.
        password_incorrect_label (tk.Label): Label indicating if the password is incorrect.

        signup_login_button (tk.Button): Button for signup or login.
        signup_login_status_label (tk.Label): Label indicating the signup or login status.

        exit_button (tk.Button): Button to exit the application.

        symbol_label (tk.Label): Label displaying a changing symbol.
        symbol_state (bool): State of the changing symbol.
    """

# -----------------------------------------------------------------
    def __init__(self, ui):
        """
        Initialize the WelcomeMenu with the given user interface.

        Parameters:
        ui (UI): The user interface instance.
        """

        print("DEBUG: Called WelcomeMenu __init__()")
        self.ui = ui
        self.done = tk.BooleanVar(value=False)  # Condition variable to signal completion
        self.user = None

        self.username_entry = None
        self.username_exists_label = None
        self.username_exists = False  # This will be used to check if the username exists

        self.password_entry = None
        self.password_incorrect_label = None

        self.signup_login_button = None
        self.signup_login_status_label = None

        self.exit_button = None

        self.symbol_label = None
        self.symbol_state = True


# -----------------------------------------------------------------
    def display(self):
        """
        Display the welcome menu.

        This method clears the current window content and creates the UI elements
        for the welcome screen.

        Example:
        Not suitable for simple doctest
        """

        print("DEBUG: Called WelcomeMenu.display()")
        # Clear the current window content
        for widget in self.ui.root.winfo_children():
            widget.destroy()

        # Create welcome menu content
        label = tk.Label(self.ui.root, text="Welcome to Sudoku!", font=("Arial", 24))
        label.pack(pady=20)
        print("DEBUG: Created and packed label")

        # Username field
        username_label = tk.Label(self.ui.root, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.ui.root)
        self.username_entry.pack(pady=5)
        self.username_entry.bind("<KeyRelease>", self.check_username)
        print("DEBUG: Created and packed username entry")

        # Username exists field
        self.username_exists_label = tk.Label(self.ui.root, text="Username exists?", fg="red")
        self.username_exists_label.pack(pady=5)
        print("DEBUG: Created and packed username exists label")

        # Password field
        password_label = tk.Label(self.ui.root, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.ui.root, show="*")
        self.password_entry.pack(pady=5)
        print("DEBUG: Created and packed password entry")

        # Password incorrect field
        self.password_incorrect_label = tk.Label(self.ui.root, text="Enter pw to check", fg="red")
        self.password_incorrect_label.pack(pady=5)
        print("DEBUG: Created and packed username exists label")

        # Signup/Login button
        self.signup_login_button = tk.Button(self.ui.root, text="Signup", command=self.signup_or_login)
        self.signup_login_button.pack(pady=10)
        print("DEBUG: Created and packed Signup/Login button")

        # Signup/Login status label
        self.signup_login_status_label = tk.Label(self.ui.root, text="Status", fg="red")
        self.signup_login_status_label.pack(pady = 5)
        print("DEBUG: Created and packed Signup/Login status label")

        # Exit button
        self.exit_button = tk.Button(self.ui.root, text="Exit", command=lambda: self.ui.root.destroy())
        self.exit_button.pack(pady=10)
        print("DEBUG: Created and packed Exit button")

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
        Not suitable for simple doctest
        """

        if self.symbol_label.winfo_exists():
            if self.symbol_state:
                self.symbol_label.config(text="/")
            else:
                self.symbol_label.config(text="\\")
            self.symbol_state = not self.symbol_state
            self.ui.root.after(1000, self.change_symbol)


# -----------------------------------------------------------------
    def check_username(self, event = None):
        """
        Check if the entered username exists.

        This method checks if the entered username exists and updates the UI elements
        accordingly.

        Example:
        Not suitable for simple doctest
        """

        print(f"DEBUG: Checking if username exists for {self.username_entry.get()}")
        self.user = SudokuUser.load_user(self.username_entry.get())
        # Add your logic here to check if the username exists
        # For now, let's simulate this with a simple condition
        if self.user:
            self.username_exists = True
            self.username_exists_label.config(text="Username already exists. Please log in.")
            self.signup_login_button.config(text="Login")
        else:
            self.username_exists = False
            self.username_exists_label.config(text="Username does not exist. Please sign up")
            self.signup_login_button.config(text="Signup")

        # self.ui.root.update()
        print(f"DEBUG: Username exists: {self.username_exists}")


# -----------------------------------------------------------------
    def signup_or_login(self):
        """
        Handle the signup or login process based on the username existence.

        This method calls either the `login` method or the `signup` method based on
        whether the username exists.

        Example:
        Not suitable for simple doctest
        """

        if self.username_exists:
            self.login()
        else:
            self.signup()


# -----------------------------------------------------------------
    def signup(self):
        """
        Handle the user signup process.

        This method creates a new user with the entered username and password,
        updates the status label, and sets the user in the UI.
        Then the method signals that it is done and the code in SudokuUI_Graphical continues.

        Example:
        Not suitable for simple doctest
        """

        self.user = SudokuUser.create_user(self.username_entry.get(), self.password_entry.get())
        self.signup_login_status_label.config(text="Creating user ...")
        print("DEBUG: Signing up...")

        self.ui.root.after(1000, lambda: self.ui.set_return_value(self.user))
        # self.ui.set_user(self.user)
        # self.done.set(True)
        # self.ui.root.after(2000, lambda: self.done.set(True)) # We use lambda so that self.done.set() is not evaluated immendiately


# -----------------------------------------------------------------
    def login(self):
        """
        Handle the user login process.

        This method verifies the entered username and password, updates the status label,
        and sets the user in the UI if the login is successful.
        Then the method signals that it is done and the code in SudokuUI_Graphical continues.

        Example:
        Not suitable for simple doctest
        """

        print("DEBUG: Checking password")
        if SudokuUser.verify_user(self.username_entry.get(), self.password_entry.get()):
            print("DEBUG: username and password match")
            self.user = SudokuUser.load_user(self.username_entry.get())
            self.signup_login_status_label.config(text="Logging into Account ...")

            self.ui.root.after(2000, lambda: self.ui.set_return_value(self.user))
            # self.ui.set_user(self.user)
            #vself.done.set(True)
            # self.ui.root.after(2000, lambda: self.done.set(True))

        else:
            print("DEBUG: username and password do NOT match")
            self.password_incorrect_label.config(text="Password incorrect. Try again.")


# -----------------------------------------------------------------

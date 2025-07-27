"""
Sudoku Terminal User Interface

This module provides a terminal-based user interface (UI) for the Sudoku game. It defines the
`SudokuUI_Terminal` class, which handles interactions with the user through a text-based interface.
This UI allows users to log in or create an account, start a new game, load a saved game, view highscores,
and perform game actions like entering moves and pausing the game.

Classes:
    SudokuUI_Terminal: A terminal-based UI for the Sudoku game.

Written by: sodonoya
"""

import datetime
import sys
from sudoku_ui import SudokuUI
from sudoku_save_load_manager import SudokuSaveLoadManager
from sudoku_highscore_manager import SudokuHighscoreManager
from sudoku_user import SudokuUser

class SudokuUI_Terminal(SudokuUI):
    """
    Terminal-based UI for the Sudoku game.

    Attributes:
        game (object): Instance of the current Sudoku game.
        user (SudokuUser): Instance of the current user.
        menu_width (int): Width of the menu for formatting purposes.
        border (str): Border string for menu formatting.
    """


# -----------------------------------------------------------------
    def __init__(self, game=None, user=None):
        """
        Initialize the terminal UI.

        Args:
            game (object, optional): The current Sudoku game instance. Defaults to None.
            user (SudokuUser, optional): The current user instance. Defaults to None.
        """
        self.game = game
        self.user = user
        self.is_graphical = False
        self.menu_width = 0
        self.border = None


# -----------------------------------------------------------------
    def set_game(self, game):
        """
        Set the current game.

        Args:
            game (object): The Sudoku game instance.
        """
        self.game = game

# -----------------------------------------------------------------
    def get_is_graphical(self):
        """
        Return info if ui is graphical
        """
        return self.is_graphical


# -----------------------------------------------------------------
    def display_welcome_menu(self):
        """
        Display the welcome menu and handle user login or account creation.

        Returns:
            SudokuUser: The current user after login or account creation.

        Raises:
            SystemExit: If the user fails to log in or chooses not to create an account.
        """
        welcome = "\n++++++++++++++++++++ WELCOME! ++++++++++++++++++++"
        print(welcome)
        self.menu_width = len(welcome.strip())

        username = input("Enter your Sudoku name: ")
        self.user = SudokuUser.load_user(username)

        # if username already exists:
        if self.user:
            for attempt in range(3):  # Allow up to 3 attempts
                password = input("Enter your password: ")
                if self.user.verify_password(password):
                    print("Login successful!")
                    print(f'Welcome back "{self.user}"!')
                    return self.user
                else:
                    print("Incorrect password, try again.")
            # After 3 fails:
            print("Too many failed attempts.")
            print("Exiting the game. Goodbye!")
            sys.exit(0)
        else:
            response = input("Username not found. Would you like to create a new account? (yes/no): ")
            if response.lower() == 'yes':
                password = input("Enter a password for your new account: ")
                self.user = SudokuUser(username)
                self.user.set_password(password)
                SudokuUser.save_user(self.user)  # SAH: Kinda redundant because we got the _init__ for SudokuUser
                print(f'New user "{self.user}" generated.')
                return self.user
            else:
                print("No account created.")
                print("Exiting the game. Goodbye!")
                sys.exit(0)



# -----------------------------------------------------------------
    def display_main_menu(self):
        """
        Display the main menu.

        Returns:
            str: User's choice from the main menu.
        """
        print("Loading main menu ...\n")
        menu_title = f" Main Menu (User: {self.user}) "

        # Calculate the number of '+' needed on each side to center the menu title
        padding_length = (self.menu_width - len(menu_title)) // 2
        filler_border = '+' * padding_length

        # Adjust the menu title to be exactly the menu_width
        menu_title = f"{filler_border}{menu_title}{filler_border}"
        if len(menu_title) < self.menu_width:
            menu_title += '+'  # Add one more '+' if the title length is odd

        print(f"{menu_title}")
        print("1. Start new game")
        print("2. Start game with AI player")
        print("3. Load unfinished game")
        print("4. Highscore")
        print("5. Exit")
        self.border = '+' * len(menu_title)
        print(self.border)

        return input("Enter your choice (1-5): ")


# -----------------------------------------------------------------
    def display_board_menu(self):
        """
        Display the current Sudoku game board.
        """
        RED = '\033[91m'
        RESET = '\033[0m'

        print(self.border)
        print(f"{self.user}'s current game | Difficulty: {self.game.get_difficulty()} / 9")
        print("+ — — — + — — — + — — — +")
        for i, row in enumerate(self.game.get_board()):
            if i % 3 == 0 and i != 0:
                print("+ — — — + — — — + — — — +")
            print("| ", end="")
            for j, cell in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                if cell['num'] == 0:
                    print(". ", end="")
                else:
                    if not cell['mutable']:  # Check if the number is from the board (given number)
                        print(f"{RED}{cell['num']}{RESET} ", end="")
                    else:
                        print(f"{cell['num']} ", end="")
            print("|")
        print("+ — — — + — — — + — — — +")
        elapsed_time = self.game.get_total_elapsed_time()
        formatted_time = str(datetime.timedelta(seconds=elapsed_time))
        print(f"Mistakes: {self.game.get_mistakes()} / 3 | Time elapsed: {formatted_time}")
        print(self.border)


# -----------------------------------------------------------------
    def display_pause_menu(self):
        """
        Display the pause menu.

        Returns:
            str: User's choice from the pause menu.
        """

        print("Loading pause menu ...\n")
        print(self.border)
        print("1. Resume game")
        print("2. Save game")
        print("3. Return to main menu")
        print(self.border)

        return input("Enter your choice (1-3): ")


# -----------------------------------------------------------------
    def display_load_menu(self):
        """
        Display the load menu for saved games.

        Returns:
            str: The selected saved game or 'return' to return to the main menu.
        """

        print("Loading load menu ...\n")
        title = " Saved games: "
        print(title.center(self.menu_width, '+'))

        saved_games = SudokuSaveLoadManager.get_list_of_saved_games(self.user)

        if saved_games:
            for i, game in enumerate(saved_games, 1):
                print(f"{i}. {game}")

            print(self.border)
            selected_game_index = input("Select a game to load (or type 'return' to return to the main menu): ")

            if selected_game_index == 'return':
                return 'return'

            try:
                selected_game_index = int(selected_game_index) - 1
                if 0 <= selected_game_index < len(saved_games):
                    selected_game = saved_games[selected_game_index]
                else:
                    self.display_message("Invalid selection: Index out of range.")
            except (IndexError, ValueError) as e:
                self.display_message(f"Invalid selection: {e}")
        else:
            print("No saved games available.")
            print(self.border)
            selected_game = input("Type 'return' to return to the main menu: ")

        return selected_game


# -----------------------------------------------------------------
    def display_highscore_menu(self):
        """
        Display the highscore menu.
        """

        print("Loading highscore menu ...\n")
        highscores = SudokuHighscoreManager.get_highscores()
        title = " Highscores: "
        print(title.center(self.menu_width, '+'))
        for user, score in highscores:
            print(f"{user}: {score}")
        print(self.border)

        while True:
            choice = input("Enter 'return' to return to main menu: ")
            if choice == 'return':
                print("Returning to main menu ...")
                return choice


# -----------------------------------------------------------------
    def get_general_input(self, prompt: str) -> str:
        """
        Get general input from the user.

        Args:
            prompt (str): The prompt message for the input.

        Returns:
            str: The user's input.
        """
        return input(prompt)


# -----------------------------------------------------------------
    def get_next_move(self):
        """
        Get the next move from the user.

        Returns:
            tuple: The row, column, and number for the next move, or 'pause' to pause the game.

        >>> ui = SudokuUI_Terminal()
        >>> ui.get_next_move()  # doctest: +SKIP
        (1, 2, 3)
        """
        row, col, num = None, 1, 1

        row = input("Enter row (1-9) or 'pause': ").strip().lower()
        if row == 'pause':
            # print(f"DEBUG: in sudoku_ui_terminal.get_next_move() - if row - row: {row}")
            return row, col, num

        row = int(row)
        col = int(input("Enter column (1-9): ").strip())
        num = int(input("Enter number (1-9) or 0 to empty a field: ").strip())

        # print(f"DEBUG: in sudoku_ui_terminal.get_next_move() - row: {row}")
        return row, col, num


# -----------------------------------------------------------------
    def display_message(self, message):
        """
        Display a message to the user.

        Args:
            message (str): The message to be displayed.

        >>> ui = SudokuUI_Terminal()
        >>> ui.display_message("Test message")
        Test message
        """
        print(message)


# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

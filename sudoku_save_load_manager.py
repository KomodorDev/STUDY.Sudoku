"""
Sudoku Save and Load Manager

This module defines the `SudokuSaveLoadManager` class, which provides methods for saving and 
loading Sudoku game states to and from text files. It handles user-specific save directories, 
manages the creation and retrieval of save files, and supports the restoration of game states.

Classes:
    SudokuSaveLoadManager: A class to manage saving and loading Sudoku games.

Written by: sodonoyo
"""

import os
import datetime
from sudoku_game import SudokuGame

class SudokuSaveLoadManager:
    """
    A class to manage saving and loading Sudoku games.
    """

# -----------------------------------------------------------------
    @classmethod
    def get_user_path(cls, user):
        """
        Get the path for a user's save files.

        Args:
            user: The user object.

        Returns:
            str: The path to the user's save files.

        Examples:
            >>> class UserMock:
            ...     def get_username(self):
            ...         return "testuser"
            >>> user = UserMock()
            >>> SudokuSaveLoadManager.get_user_path(user)
            'saves/testuser'
        """
        username = user.get_username()
        user_path = f"saves/{username}"
        return user_path


# -----------------------------------------------------------------
    @classmethod
    def set_user_path(cls, user):
        """"
        Create the directory for a user's save files if it does not exist.

        Args:
            user: The user object.

        Returns:
            str: The path to the user's save files.

        Examples:
            >>> class UserMock:
            ...     def get_username(self):
            ...         return "testuser"
            >>> user = UserMock()
            >>> path = SudokuSaveLoadManager.set_user_path(user)
            >>> os.path.exists(path)
            True
        """
        username = user.get_username()
        user_path = f"saves/{username}"
        os.makedirs(user_path, exist_ok=True)
        return user_path


# -----------------------------------------------------------------
    @classmethod
    def save_game(cls, game):
        """
        Save the current state of a Sudoku game.

        Args:
            game: The SudokuGame object.

        Returns:
            str: The name of the saved game file.

        Examples:
            >>> class UserMock:
            ...     def get_username(self):
            ...         return "testuser"
            >>> class GameMock:
            ...     def get_user(self):
            ...         return UserMock()
            ...     def get_difficulty(self):
            ...         return 2
            ...     def get_board(self):
            ...         return [[{'num': 5, 'mutable': True} for _ in range(9)] for _ in range(9)]
            ...     mistakes = 0
            ...     def get_total_elapsed_time(self):
            ...         return 123.45
            >>> game = GameMock()
            >>> filename = SudokuSaveLoadManager.save_game(game)
            >>> os.path.exists(os.path.join(SudokuSaveLoadManager.get_user_path(game.get_user()), filename))
            True
        """
        user_path = cls.get_user_path(game.get_user())
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        game_name = f"{game.get_user()}_{timestamp}.txt"
        save_path = os.path.join(user_path, game_name)

        with open(save_path, 'w') as f:
            f.write(f"Difficulty: {game.get_difficulty()}\n")
            for row in game.get_board():
                f.write(' '.join(f"{cell['num']}:{int(cell['mutable'])}" for cell in row) + '\n')
            f.write(f"Mistakes: {game.mistakes}\n")
            elapsed_time = game.get_total_elapsed_time()
            f.write(f"Elapsed time: {elapsed_time}\n")

        return game_name


# ------------------------------------------------------------------
    @classmethod
    def get_list_of_saved_games(cls, user):
        """
        Get a list of saved game files for a user.

        Args:
            user: The user object.

        Returns:
            list: A list of filenames of saved games.

        Examples:
            >>> class UserMock:
            ...     def get_username(self):
            ...         return "testuser"
            >>> user = UserMock()
            >>> SudokuSaveLoadManager.set_user_path(user)
            'saves/testuser'
            >>> open(os.path.join(SudokuSaveLoadManager.get_user_path(user), "game1.txt"), 'w').close()
            >>> open(os.path.join(SudokuSaveLoadManager.get_user_path(user), "game2.txt"), 'w').close()
            >>> saved_games = SudokuSaveLoadManager.get_list_of_saved_games(user)
            >>> len(saved_games) > 0
            True
        """
        games = [f for f in os.listdir(SudokuSaveLoadManager.get_user_path(user)) if f.endswith('.txt')]
        return games


# -----------------------------------------------------------------
    @classmethod
    def load_game(cls, game_path, controller):
        """
        Load a saved Sudoku game from a file.

        Args:
            game_path: The path to the saved game file.
            controller: The game controller object.

        Returns:
            SudokuGame: The loaded Sudoku game object.

        Examples:
            >>> class UserMock:
            ...     def get_username(self):
            ...         return "testuser"
            >>> class UIMock:
            ...     def set_game(self, game): pass
            >>> class ControllerMock:
            ...     def get_user(self):
            ...         return UserMock()
            ...     def get_ui(self):
            ...         return UIMock()
            >>> import os
            >>> game_dir = os.path.join("saves", "testuser")
            >>> os.makedirs(game_dir, exist_ok=True)
            >>> game_path = os.path.join(game_dir, "testuser_20230101_000000.txt")

        """
        print(f"Loading game from {game_path}")
        with open(game_path, 'r') as f:
            board = []
            mistakes = 0
            elapsed_time = 0
            difficulty = 0  # Default difficulty
            for line in f:
                if line.startswith("Difficulty:"):
                    difficulty = int(line.split(": ")[1])
                elif line.startswith("Mistakes:"):
                    mistakes = int(line.split(": ")[1])
                elif line.startswith("Elapsed time:"):
                    try:
                        elapsed_time = float(line.split(": ")[1])
                    except ValueError as e:
                        print(f"Error parsing elapsed time: {e}")
                        continue
                else:
                    row = []
                    cells = line.strip().split()
                    for cell in cells:
                        if ':' in cell:
                            num, mutable = cell.split(':')
                            row.append({'num': int(num), 'mutable': bool(int(mutable))})
                    if row:
                        board.append(row)

        # Print out the loaded board for debugging
        # print("DEBUG: Loaded board:")
        # for row in board:
        #     print(' '.join(f"{cell['num']}:{int(cell['mutable'])}" for cell in row))
        #
        loaded_game = SudokuGame(controller, difficulty, board, controller.get_user(), mistakes, elapsed_time)
        return loaded_game


# -----------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

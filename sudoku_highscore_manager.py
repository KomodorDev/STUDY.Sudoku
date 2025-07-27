"""
Module for managing high scores in the Sudoku game.

This module provides the `SudokuHighscoreManager` class, which includes methods to get, set,
and manage high scores stored in a text file.

Classes:
    SudokuHighscoreManager

Written by: hintsimo (Komodorpudel)
"""

import os

class SudokuHighscoreManager:
    """
    Class for managing high scores in the Sudoku game.

    This class provides methods to get, set, and manage high scores stored in a text file.

    Attributes:
    HIGHSCORE_FILE (str): The name of the file where high scores are stored.
    """

    HIGHSCORE_FILE = "highscores.txt"

# -----------------------------------------------------------------
    @classmethod
    def get_highscores(cls):
        """
        Retrieve the list of high scores from the high score file.

        Returns:
        list of tuples: A list of tuples, where each tuple contains a username and their score.

        Example:
        >>> temp_file = "temp_highscores.txt"
        >>> SudokuHighscoreManager.HIGHSCORE_FILE = temp_file
        >>> with open(SudokuHighscoreManager.HIGHSCORE_FILE, 'w') as f:
        ...     _ = f.write('Alice:150\\nBob:200\\n')
        >>> SudokuHighscoreManager.get_highscores()
        [('Alice', 150), ('Bob', 200)]
        >>> os.remove(temp_file)
        """
        if not os.path.exists(cls.HIGHSCORE_FILE):
            return []
        highscores = []
        try:
            with open(cls.HIGHSCORE_FILE, 'r') as f:
                for line in f:
                    try:
                        if ':' in line:
                            user, scr = line.strip().split(':')
                            highscores.append((user, int(scr)))
                    except ValueError as e:
                        print(f"DEBUG: Error parsing line '{line.strip()}': {e}")
        except Exception as e:
            print(f"DEBUG: Error reading highscores file: {e}")
        return highscores


# -----------------------------------------------------------------
    @classmethod
    def get_user_highscore(cls, user):
        """
        Retrieve the high score for a specific user.

        Parameters:
        user (User): The user object with a get_username method.

        Returns:
        int: The high score for the user. Returns 0 if the user has no high score.

        Example:
        >>> class MockUser:
        ...     def get_username(self):
        ...         return 'Alice'
        >>> temp_file = "temp_highscores.txt"
        >>> SudokuHighscoreManager.HIGHSCORE_FILE = temp_file
        >>> with open(SudokuHighscoreManager.HIGHSCORE_FILE, 'w') as f:
        ...     _ = f.write('Alice:150\\nBob:200\\n')
        >>> user = MockUser()
        >>> SudokuHighscoreManager.get_user_highscore(user)
        150
        >>> os.remove(temp_file)
        """

        highscores = cls.get_highscores()
        username = user.get_username()
        for u, score in highscores:
            if u == username:
                return score
        return 0


# -----------------------------------------------------------------
    @classmethod
    def set_highscore(cls, user, score):
        """
        Set or update the high score for a user.

        Parameters:
        user (User): The user object with a get_username method.
        score (int): The score to be added to the user's high score.

        Returns:
        int: The new high score for the user.

        Example:
        >>> class MockUser:
        ...     def get_username(self):
        ...         return 'Alice'
        >>> temp_file = "temp_highscores.txt"
        >>> SudokuHighscoreManager.HIGHSCORE_FILE = temp_file
        >>> with open(SudokuHighscoreManager.HIGHSCORE_FILE, 'w') as f:
        ...     _ = f.write('Alice:150\\nBob:200\\n')
        >>> user = MockUser()
        >>> SudokuHighscoreManager.set_highscore(user, 50)
        >>> SudokuHighscoreManager.get_user_highscore(user)
        200
        >>> os.remove(temp_file)
        """

        highscores = cls.get_highscores()
        user_found = False
        username = user.get_username()
        for i, (u, scr) in enumerate(highscores):
            if u == username:
                highscores[i] = (username, scr + score)
                user_found = True
                break
        if not user_found:
            highscores.append((username, score))

        cls._save_highscores(highscores)

# -----------------------------------------------------------------
    @classmethod
    def _save_highscores(cls, highscores):
        """
        Save the high scores to the high score file.

        Parameters:
        highscores (dict): A dictionary with usernames as keys and scores as values.

        Example:
        >>> highscores = [('Alice', 150), ('Bob', 200)]
        >>> temp_file = "temp_highscores.txt"
        >>> SudokuHighscoreManager.HIGHSCORE_FILE = temp_file
        >>> SudokuHighscoreManager._save_highscores(highscores)
        >>> with open(SudokuHighscoreManager.HIGHSCORE_FILE, 'r') as f:
        ...     lines = f.readlines()
        >>> lines
        ['Bob:200\\n', 'Alice:150\\n']
        >>> os.remove(temp_file)
        """

        highscores.sort(key=lambda x: x[1], reverse=True)
        with open(cls.HIGHSCORE_FILE, 'w') as file:
            for username, score in highscores:
                file.write(f"{username}:{score}\n")


# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

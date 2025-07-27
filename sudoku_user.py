"""
A module for managing Sudoku game users with secure password handling.

Classes:
    SudokuUser: Represents a user of the Sudoku game with methods for password management and database operations.

Written by: hintsimo (Komodorpudel)
"""

import shelve
import bcrypt

class SudokuUser:
    """
    Represents a user of the Sudoku game.

    Attributes:
        username (str): The username of the user.
        password_hash (bytes): The hashed password of the user.

    Methods:
        get_username(): Returns the username of the user.
        set_password(password): Hashes and sets the user's password.
        verify_password(password): Verifies that a provided password matches the stored hash.
        __str__(): Returns the username as the string representation of the object.
        create_user(username, password): Creates a new user with a hashed password and saves it to the database.
        load_user(username): Loads a user from storage.
        verify_user(username, password): Verifies user's password against the stored hash.
        save_user(user): Saves the user object to the database.
    """

# -----------------------------------------------------------------
    def __init__(self, username, password_hash=None):
        """
        Constructs all the necessary attributes for the SudokuUser object.

        Parameters:
        username (str): The username of the user.
        password_hash (bytes, optional): The hashed password of the user (default is None).

        Example:
        >>> user = SudokuUser('john_doe')
        >>> user.username
        'john_doe'
        """

        self.username = username
        self.password_hash = password_hash

# -----------------------------------------------------------------
    def get_username(self):
        """
        Gets the username of the user.

        Returns:
        str: The username of the user.

        Example:
        >>> user = SudokuUser('john_doe')
        >>> user.get_username()
        'john_doe'
        """

        return self.username


# -----------------------------------------------------------------
    def set_password(self, password):
        """
        Gets the username of the user.

        Returns:
        str: The username of the user.

        Example:
        >>> user = SudokuUser('john_doe')
        >>> user.get_username()
        'john_doe'
        """

        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


# -----------------------------------------------------------------
    def verify_password(self, password):
        """
        Verifies that a provided password matches the stored hash.

        Parameters:
        password (str): The password to verify.

        Returns:
        bool: True if the password matches the stored hash, False otherwise.

        Example:
        >>> user = SudokuUser('john_doe')
        >>> user.set_password('secure_password')
        >>> user.verify_password('secure_password')
        True
        >>> user.verify_password('wrong_password')
        False
        """

        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


# -----------------------------------------------------------------
    def __str__(self):
        """
        Returns the username as the string representation of the object.

        Returns:
        str: The username of the user.

        Example:
        >>> user = SudokuUser('john_doe')
        >>> str(user)
        'john_doe'
        """

        return self.username


# -----------------------------------------------------------------
    @classmethod
    def create_user(cls, username, password):
        """
        Creates a new user with a hashed password and saves it to the database.

        Parameters:
        username (str): The username of the new user.
        password (str): The password of the new user.

        Returns:
        SudokuUser: The created user object.

        Example:
        >>> user = SudokuUser.create_user('john_doe', 'secure_password')
        >>> user.username
        'john_doe'
        >>> user.verify_password('secure_password')
        True
        """

        user = cls(username) # Create a new user
        user.set_password(password) # Set hashed pw for that user
        cls.save_user(user) # we save user in database
        return user


# -----------------------------------------------------------------
    @classmethod
    def load_user(cls, username):
        """
        Loads a user from storage.

        Parameters:
        username (str): The username of the user to load.

        Returns:
        SudokuUser or None: The loaded user object if found, None otherwise.

        Example:
        >>> user = SudokuUser.create_user('john_doe', 'secure_password')
        >>> loaded_user = SudokuUser.load_user('john_doe')
        >>> loaded_user.username
        'john_doe'
        >>> loaded_user.verify_password('secure_password')
        True
        """

        with shelve.open('sudoku_users') as db:
            if username in db:
                user_data = db[username]
                return cls(username, user_data['password_hash'])
        return None


# -----------------------------------------------------------------
    @classmethod
    def verify_user(cls, username, password):
        """
        Verifies user's password against the stored hash.

        Parameters:
        username (str): The username of the user.
        password (str): The password to verify.

        Returns:
        bool: True if the password matches the stored hash, False otherwise.

        Example:
        >>> user = SudokuUser.create_user('john_doe', 'secure_password')
        >>> SudokuUser.verify_user('john_doe', 'secure_password')
        True
        >>> SudokuUser.verify_user('john_doe', 'wrong_password')
        False
        """

        user = cls.load_user(username)
        if user and user.verify_password(password):
            return True
        return False


# -----------------------------------------------------------------
    @classmethod
    def save_user(cls, user):
        """
        Saves the user object to the database.

        Parameters:
        user (SudokuUser): The user object to save.

        Example:
        >>> user = SudokuUser('john_doe')
        >>> user.set_password('secure_password')
        >>> SudokuUser.save_user(user)
        >>> loaded_user = SudokuUser.load_user('john_doe')
        >>> loaded_user.username
        'john_doe'
        """

        with shelve.open('sudoku_users') as db:
            db[user.username] = {'password_hash': user.password_hash}


# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

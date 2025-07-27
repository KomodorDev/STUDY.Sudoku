"""
Sudoku Board Generator Module

This module provides the `SudokuBoardGenerator` class to generate Sudoku boards of varying difficulty levels.
It includes methods for generating a full board, validating placements, and removing numbers to create puzzles of different difficulties.

Classes:
    SudokuBoardGenerator: Generates and modifies Sudoku boards.

Written by: bayosoun
"""

import random

class SudokuBoardGenerator:
    """
    Generates and modifies Sudoku boards of varying difficulty levels.

    The SudokuBoardGenerator class includes methods for generating a complete Sudoku board,
    validating placements of numbers according to Sudoku rules, and removing numbers to create
    puzzles of different difficulties.

    Attributes:
        board (list): A 9x9 grid representing the Sudoku board, where each cell is a dictionary
                      with 'num' (the number) and 'mutable' (whether the number can be changed).

    Methods:
        __init__(difficulty=0):
            Initializes a Sudoku board generator with a given difficulty level.

        generate_full_board():
            Generates a complete, valid Sudoku board.

        valid_placement(row, col, num):
            Checks if placing a number in a specific position is valid according to Sudoku rules.

        remove_numbers(difficulty):
            Removes numbers from the fully generated Sudoku board based on the difficulty level.

        remove_simple():
            Removes numbers from the board to create a simple Sudoku puzzle.

        is_solvable():
            Checks if the current board configuration is solvable.

        solve_with_simple_techniques(board):
            Solves the board using simple techniques (Single Candidate, Single Position).

        single_candidate(board):
            Applies the Single Candidate technique to the board.

        single_position(board):
            Applies the Single Position technique to the board.

        remove_medium():
            Removes numbers from the board to create a medium Sudoku puzzle.

        is_solvable_with_medium_techniques():
            Checks if the current board configuration is solvable using medium techniques.

        solve_with_medium_techniques(board):
            Solves the board using medium techniques (Single Candidate, Single Position, Naked Pairs, Pointing Pairs).

        naked_pairs(board):
            Applies the Naked Pairs technique to the board.

        pointing_pairs(board):
            Applies the Pointing Pairs technique to the board.

        remove_hard():
            Removes numbers from the board to create a hard Sudoku puzzle.

        is_solvable_with_hard_techniques():
            Checks if the current board configuration is solvable using hard techniques.

        solve_with_hard_techniques(board):
            Solves the board using hard techniques (Single Candidate, Single Position, Naked Pairs, Pointing Pairs, X-Wing).

        x_wing(board):
            Applies the X-Wing technique to the board.

        get_board():
            Returns a copy of the current Sudoku board.

        generate_board(difficulty=0):
            Generates a Sudoku board with the given difficulty.
    """

# -----------------------------------------------------------------
    def __init__(self, difficulty=0):
        """
        Initializes a Sudoku board generator with a given difficulty level.

        Args:
            difficulty (int): The difficulty level for the Sudoku puzzle (default is 0).

        Raises:
            ValueError: If a valid Sudoku board cannot be generated.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=1)
            >>> len(generator.board)
            9
            >>> len(generator.board[0])
            9
        """
        self.board = [[{'num': 0, 'mutable': True} for _ in range(9)] for _ in range(9)]
        if not self.generate_full_board():
            raise ValueError("Failed to generate a valid Sudoku board.")
        self.remove_numbers(difficulty)


# -----------------------------------------------------------------
    def generate_full_board(self):
        """
        Generates a complete, valid Sudoku board.

        Returns:
            bool: True if the board is successfully generated, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
        """

        def fill(position=0):
            if position == 81:
                return True
            row, col = divmod(position, 9)
            if self.board[row][col]['num'] == 0:
                random_numbers = list(range(1, 10))
                random.shuffle(random_numbers)
                for number in random_numbers:
                    if self.valid_placement(row, col, number):
                        self.board[row][col]['num'] = number
                        if fill(position + 1):
                            return True
                        self.board[row][col]['num'] = 0
            else:
                return fill(position + 1)
            return False
        return fill()


# -----------------------------------------------------------------
    def valid_placement(self, row, col, num):
        """
        Checks if placing a number in a specific position is valid according to Sudoku rules.

        Args:x
            row (int): The row index of the position.
            col (int): The column index of the position.
            num (int): The number to place.

        Returns:
            bool: True if the placement is valid, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.valid_placement(0, 0, 5)
            True
        """

        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        if any(self.board[row][i]['num'] == num for i in range(9)):
            return False
        if any(self.board[i][col]['num'] == num for i in range(9)):
            return False
        if any(self.board[r][c]['num'] == num for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3)):
            return False
        return True


# -----------------------------------------------------------------
    def remove_numbers(self, difficulty):
        """
        Removes numbers from the fully generated Sudoku board based on the difficulty level.

        Args:
            difficulty (int): The difficulty level for the Sudoku puzzle.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.remove_numbers(3)
            >>> sum(cell['num'] == 0 for row in generator.board for cell in row) > 0
            True
        """

        if difficulty < 5:
            self.remove_simple()
        elif difficulty < 10:
            self.remove_medium()
        # elif difficulty < 10:
        #     self.remove_hard()


# -----------------------------------------------------------------
    def remove_simple(self):
        """
        Removes numbers from the board to create a simple Sudoku puzzle.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.remove_simple()
            >>> sum(cell['num'] == 0 for row in generator.board for cell in row) >= 36
            True
        """

        cells_to_keep = 45  # Anzahl der zu behaltenden Zellen für einfaches Puzzle
        cells_to_remove = 81 - cells_to_keep

        while cells_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col]['num'] != 0:
                backup = self.board[row][col]['num']
                self.board[row][col]['num'] = 0
                if self.is_solvable():
                    cells_to_remove -= 1
                else:
                    self.board[row][col]['num'] = backup

        # Set immutability for the remaining cells
        for row in self.board:
            for cell in row:
                if cell['num'] != 0:
                    cell['mutable'] = False


# -----------------------------------------------------------------
    def is_solvable(self):
        """
        Checks if the current board configuration is solvable.

        Returns:
            bool: True if the board is solvable, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.is_solvable()
            True
        """

        board_copy = self.get_board()
        return self.solve_with_simple_techniques(board_copy)


# -----------------------------------------------------------------
    def solve_with_simple_techniques(self, board):
        """
        Solves the board using simple techniques (Single Candidate, Single Position).
        Returns True if solvable with simple techniques, False otherwise.

        Args:
            board (list): The Sudoku board to solve.

        Returns:
            bool: True if the board is solvable with simple techniques, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> generator.solve_with_simple_techniques(board)
            True
        """

        while True:
            changes = False
            if self.single_candidate(board):
                changes = True
            if self.single_position(board):
                changes = True
            if not changes:
                break
        return all(all(cell['num'] != 0 for cell in row) for row in board)


# -----------------------------------------------------------------
    def single_candidate(self, board):
        """
        Applies the Single Candidate technique to the board.
        Returns True if any changes were made, False otherwise.

        Args:
            board (list): The Sudoku board to apply the technique on.

        Returns:
            bool: True if any changes were made, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> generator.single_candidate(board)
            True
        """

        changes_made = False
        for row in range(9):
            for col in range(9):
                if board[row][col]['num'] == 0:
                    possible_numbers = [num for num in range(1, 10) if self.valid_placement(row, col, num)]
                    if len(possible_numbers) == 1:
                        board[row][col]['num'] = possible_numbers[0]
                        changes_made = True
        return changes_made


# -----------------------------------------------------------------
    def single_position(self, board):
        """
        Applies the Single Position technique to the board.
        Returns True if any changes were made, False otherwise.

        Args:
            board (list): The Sudoku board to apply the technique on.

        Returns:
            bool: True if any changes were made, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> generator.single_position(board)
            True
        """

        changes_made = False
        for num in range(1, 10):
            # Check rows
            for row in range(9):
                possible_positions = [col for col in range(9) if board[row][col]['num'] == 0 and self.valid_placement(row, col, num)]
                if len(possible_positions) == 1:
                    board[row][possible_positions[0]]['num'] = num
                    changes_made = True

            # Check columns
            for col in range(9):
                possible_positions = [row for row in range(9) if board[row][col]['num'] == 0 and self.valid_placement(row, col, num)]
                if len(possible_positions) == 1:
                    board[possible_positions[0]][col]['num'] = num
                    changes_made = True

            # Check blocks
            for block_row in range(0, 9, 3):
                for block_col in range(0, 9, 3):
                    possible_positions = [(r, c) for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3) if board[r][c]['num'] == 0 and self.valid_placement(r, c, num)]
                    if len(possible_positions) == 1:
                        r, c = possible_positions[0]
                        board[r][c]['num'] = num
                        changes_made = True

        return changes_made


# -----------------------------------------------------------------
    def remove_medium(self):
        """
        Removes numbers from the board to create a medium Sudoku puzzle.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.remove_medium()
            >>> sum(cell['num'] == 0 for row in generator.board for cell in row) >= 45
            True
        """

        cells_to_keep = 36  # Anzahl der zu behaltenden Zellen für mittleres Puzzle
        cells_to_remove = 81 - cells_to_keep

        while cells_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col]['num'] != 0:
                backup = self.board[row][col]['num']
                self.board[row][col]['num'] = 0
                if self.is_solvable_with_medium_techniques():
                    cells_to_remove -= 1
                else:
                    self.board[row][col]['num'] = backup

        # Set immutability for the remaining cells
        for row in self.board:
            for cell in row:
                if cell['num'] != 0:
                    cell['mutable'] = False


# -----------------------------------------------------------------
    def is_solvable_with_medium_techniques(self):
        """
        Checks if the current board configuration is solvable using medium techniques.

        Returns:
            bool: True if the board is solvable using medium techniques, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.is_solvable_with_medium_techniques()
            True
        """

        board_copy = self.get_board()
        return self.solve_with_medium_techniques(board_copy)


# -----------------------------------------------------------------
    def solve_with_medium_techniques(self, board):
        """
        Solves the board using medium techniques (Single Candidate, Single Position, Naked Pairs, Pointing Pairs).
        Returns True if solvable with medium techniques, False otherwise.

        Args:
            board (list): The Sudoku board to solve.

        Returns:
            bool: True if the board is solvable with medium techniques, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> generator.solve_with_medium_techniques(board)
            True
        """

        while True:
            changes = False
            if self.single_candidate(board):
                changes = True
            if self.single_position(board):
                changes = True
            if self.naked_pairs(board):
                changes = True
            if self.pointing_pairs(board):
                changes = True
            if not changes:
                break
        return all(all(cell['num'] != 0 for cell in row) for row in board)


# -----------------------------------------------------------------
    def naked_pairs(self, board):
        """
        Applies the Naked Pairs technique to the board.
        Returns True if any changes were made, False otherwise.

        Args:
            board (list): The Sudoku board to apply the technique on.

        Returns:
            bool: True if any changes were made, False otherwise.

        """

        changes_made = False

        # Check rows
        for row in range(9):
            pairs = {}
            for col in range(9):
                if board[row][col]['num'] == 0:
                    possible_numbers = [num for num in range(1, 10) if self.valid_placement(row, col, num)]
                    if len(possible_numbers) == 2:
                        pair = tuple(possible_numbers)
                        if pair in pairs:
                            # Found a naked pair
                            for c in range(9):
                                if c != col and c != pairs[pair] and board[row][c]['num'] == 0:
                                    for num in pair:
                                        if num in [n for n in range(1, 10) if self.valid_placement(row, c, n)]:
                                            board[row][c]['num'] = 0
                                            changes_made = True
                        else:
                            pairs[pair] = col

        # Check columns
        for col in range(9):
            pairs = {}
            for row in range(9):
                if board[row][col]['num'] == 0:
                    possible_numbers = [num for num in range(1, 10) if self.valid_placement(row, col, num)]
                    if len(possible_numbers) == 2:
                        pair = tuple(possible_numbers)
                        if pair in pairs:
                            # Found a naked pair
                            for r in range(9):
                                if r != row and r != pairs[pair] and board[r][col]['num'] == 0:
                                    for num in pair:
                                        if num in [n for n in range(1, 10) if self.valid_placement(r, col, n)]:
                                            board[r][col]['num'] = 0
                                            changes_made = True
                        else:
                            pairs[pair] = row

        return changes_made


# -----------------------------------------------------------------
    def pointing_pairs(self, board):
        """
        Applies the Pointing Pairs technique to the board.
        Returns True if any changes were made, False otherwise.

        Args:
            board (list): The Sudoku board to apply the technique on.

        Returns:
            bool: True if any changes were made, False otherwise.
        """

        changes_made = False

        for num in range(1, 10):
            # Check rows in blocks
            for block_row in range(0, 9, 3):
                for block_col in range(0, 9, 3):
                    positions = []
                    for r in range(block_row, block_row + 3):
                        for c in range(block_col, block_col + 3):
                            if board[r][c]['num'] == 0 and self.valid_placement(r, c, num):
                                positions.append((r, c))
                    if len(positions) == 2 or len(positions) == 3:
                        if all(pos[0] == positions[0][0] for pos in positions):
                            row = positions[0][0]
                            for col in range(9):
                                if col < block_col or col >= block_col + 3:
                                    if self.valid_placement(row, col, num):
                                        board[row][col]['num'] = 0
                                        changes_made = True

            # Check columns in blocks
            for block_row in range(0, 9, 3):
                for block_col in range(0, 9, 3):
                    positions = []
                    for r in range(block_row, block_row + 3):
                        for c in range(block_col, block_col + 3):
                            if board[r][c]['num'] == 0 and self.valid_placement(r, c, num):
                                positions.append((r, c))
                    if len(positions) == 2 or len(positions) == 3:
                        if all(pos[1] == positions[0][1] for pos in positions):
                            col = positions[0][1]
                            for row in range(9):
                                if row < block_row or row >= block_row + 3:
                                    if self.valid_placement(row, col, num):
                                        board[row][col]['num'] = 0
                                        changes_made = True

        return changes_made

# -----------------------------------------------------------------
    def remove_hard(self):
        """
        Removes numbers from the board to create a hard Sudoku puzzle.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.remove_hard()
            >>> sum(cell['num'] == 0 for row in generator.board for cell in row) >= 53
            True
        """

        cells_to_keep = 28  # Anzahl der zu behaltenden Zellen für schweres Puzzle
        cells_to_remove = 81 - cells_to_keep

        while cells_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col]['num'] != 0:
                backup = self.board[row][col]['num']
                self.board[row][col]['num'] = 0
                if self.is_solvable_with_hard_techniques():
                    cells_to_remove -= 1
                else:
                    self.board[row][col]['num'] = backup

        # Set immutability for the remaining cells
        for row in self.board:
            for cell in row:
                if cell['num'] != 0:
                    cell['mutable'] = False


# -----------------------------------------------------------------
    def is_solvable_with_hard_techniques(self):
        """
        Checks if the current board configuration is solvable using hard techniques.

        Returns:
            bool: True if the board is solvable using hard techniques, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> generator.is_solvable_with_hard_techniques()
            True
        """

        board_copy = self.get_board()
        return self.solve_with_hard_techniques(board_copy)


# -----------------------------------------------------------------
    def solve_with_hard_techniques(self, board):
        """
        Solves the board using hard techniques (Single Candidate, Single Position, Naked Pairs, Pointing Pairs, X-Wing).
        Returns True if solvable with hard techniques, False otherwise.

        Args:
            board (list): The Sudoku board to solve.

        Returns:
            bool: True if the board is solvable with hard techniques, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> generator.solve_with_hard_techniques(board)
            True
        """

        while True:
            changes = False
            if self.single_candidate(board):
                changes = True
            if self.single_position(board):
                changes = True
            if self.naked_pairs(board):
                changes = True
            if self.pointing_pairs(board):
                changes = True
            if self.x_wing(board):
                changes = True
            if not changes:
                break
        return all(all(cell['num'] != 0 for cell in row) for row in board)


# -----------------------------------------------------------------
    def x_wing(self, board):
        """
        Applies the X-Wing technique to the board.
        Returns True if any changes were made, False otherwise.

        Args:
            board (list): The Sudoku board to apply the technique on.

        Returns:
            bool: True if any changes were made, False otherwise.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> generator.x_wing(board)
            False  # This will typically be False unless the board setup specifically needs X-Wing
        """

        changes_made = False

        def check_x_wing(lines, get_index):
            nonlocal changes_made
            for num in range(1, 10):
                positions = [[] for _ in range(9)]
                for line in range(9):
                    for index in range(9):
                        row, col = get_index(line, index)  # Entpacke das Tupel hier
                        if board[row][col]['num'] == 0 and self.valid_placement(row, col, num):
                            positions[line].append(index)
                    if len(positions[line]) == 2:
                        for other_line in range(line + 1, 9):
                            if positions[line] == positions[other_line]:
                                for index in range(9):
                                    if index != positions[line][0] and index != positions[line][1]:
                                        row, col = get_index(line, index)  # Entpacke das Tupel hier
                                        if self.valid_placement(row, col, num):
                                            board[row][col]['num'] = 0
                                            changes_made = True
                                        row, col = get_index(other_line, index)  # Entpacke das Tupel hier
                                        if self.valid_placement(row, col, num):
                                            board[row][col]['num'] = 0
                                            changes_made = True

        # Check rows for X-Wing
        check_x_wing(range(9), lambda row, col: (row, col))

        # Check columns for X-Wing
        check_x_wing(range(9), lambda col, row: (row, col))

        return changes_made


# -----------------------------------------------------------------
    def get_board(self):
        """
        Returns a copy of the current Sudoku board.

        Returns:
            list: A 9x9 copy of the current Sudoku board.

        Examples:
            >>> generator = SudokuBoardGenerator(difficulty=0)
            >>> generator.generate_full_board()
            True
            >>> board = generator.get_board()
            >>> len(board)
            9
            >>> len(board[0])
            9
        """

        return [[cell.copy() for cell in row] for row in self.board]


# -----------------------------------------------------------------
    @classmethod
    def generate_board(cls, difficulty=0):
        """
        Generates a Sudoku board with the given difficulty.

        Args:
            difficulty (int): The difficulty level for the Sudoku puzzle (default is 0).

        Returns:
            list: A 9x9 Sudoku board.

        Examples:
            >>> board = SudokuBoardGenerator.generate_board(difficulty=1)
            >>> len(board)
            9
            >>> len(board[0])
            9
        """

        generator = cls(difficulty)
        return generator.get_board()


# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------
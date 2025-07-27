"""
Sudoku Stopwatch Module

This module provides a simple stopwatch class (`SudokuStopwatch`) to measure elapsed time.
It is used for tracking the time spent on a Sudoku game.

Classes:
    SudokuStopwatch: A simple stopwatch to measure elapsed time.

Written by: bayosoun
"""

import time

class SudokuStopwatch:
    '''
    A simple stopwatch to measure elapsed time.

    Attributes:
    start_time (float): The start time of the stopwatch.
    elapsed_time (float): The total elapsed time when the stopwatch is paused.

    Methods:
    start(): Starts the stopwatch.
    pause(): Pauses the stopwatch.
    reset(): Resets the stopwatch.
    get_elapsed_time(): Returns the total elapsed time.
    '''
# -----------------------------------------------------------------
    def __init__(self):
        '''
        Initializes the stopwatch with start time as None and elapsed time as 0.

        Examples:
        >>> stopwatch = SudokuStopwatch()
        >>> stopwatch.start_time is None
        True
        >>> stopwatch.elapsed_time
        0
        '''

        self.start_time = None
        self.elapsed_time = 0


# -----------------------------------------------------------------
    def start(self):
        '''
        Starts the stopwatch. If the stopwatch is already running, it does nothing.

        Examples:
        >>> stopwatch = SudokuStopwatch()
        >>> stopwatch.start()
        >>> isinstance(stopwatch.start_time, float)
        True
        '''

        if self.start_time is None:
            self.start_time = time.time()


# -----------------------------------------------------------------
    def pause(self):
        '''
        Pauses the stopwatch and adds the time elapsed since it was started to the total elapsed time.

        Examples:
        >>> stopwatch = SudokuStopwatch()
        >>> stopwatch.start()
        >>> time.sleep(1)
        >>> stopwatch.pause()
        >>> 0.9 < stopwatch.get_elapsed_time() < 1.1
        True
        '''

        if self.start_time is not None:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None


# -----------------------------------------------------------------
    def reset(self):
        '''
        Resets the stopwatch to its initial state.

        Examples:
        >>> stopwatch = SudokuStopwatch()
        >>> stopwatch.start()
        >>> time.sleep(1)
        >>> stopwatch.reset()
        >>> stopwatch.elapsed_time
        0
        '''


# -----------------------------------------------------------------
    def get_elapsed_time(self):
        '''
        Returns the total elapsed time. If the stopwatch is running, it includes the time elapsed since it was started.

        Returns:
        float: The total elapsed time in seconds.

        Examples:
        >>> stopwatch = SudokuStopwatch()
        >>> stopwatch.start()
        >>> time.sleep(1)
        >>> 0.9 < stopwatch.get_elapsed_time() < 1.1
        True
        >>> stopwatch.pause()
        >>> stopwatch.get_elapsed_time() > 0.9
        True
        '''

        if self.start_time is not None:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

# -----------------------------------------------------------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


# -----------------------------------------------------------------

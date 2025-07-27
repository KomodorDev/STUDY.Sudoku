"""
Main module for starting the Sudoku application.

Functions:
    main: The main function to start the Sudoku application.

Written by: hintsimo (Komodorpudel)
"""

import sys

# -----------------------------------------------------------------
def main():
    """
    The main function to start the Sudoku application.

    This function prompts the user to select their preferred UI type (Graphical or Terminal).
    Depending on the user's input, it imports and initializes the appropriate UI class
    (SudokuUI_Graphical or SudokuUI_Terminal). If the input is invalid, it exits the program
    with an error message.

    Once the UI is selected, the function initializes the SudokuAppController with the chosen UI
    and runs the welcome menu of the Sudoku application.

    Usage:
        - Run the script and follow the prompt to choose either 'gui' or 'terminal'.
        - The script will import the corresponding UI module and initialize the Sudoku application.
    """

    # Ask the user for their preferred UI type:
    ui_type = input("Which UI would you like to use? (Enter 'gui' or 'terminal'): ").strip().lower()

    if ui_type == 'gui':
        from sudoku_ui_graphical import SudokuUI_Graphical
        ui = SudokuUI_Graphical()
    elif ui_type == 'terminal':
        from sudoku_ui_terminal import SudokuUI_Terminal
        ui = SudokuUI_Terminal()
    else:
        print("Invalid input. Exiting...")
        sys.exit(1)

    from sudoku_app_controller import SudokuAppController
    controller = SudokuAppController(ui)
    controller.run_welcome_menu()

# -----------------------------------------------------------------
if __name__ == "__main__":
    main()

# -----------------------------------------------------------------

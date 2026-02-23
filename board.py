"""
board.py

Contains the Board class which manages the Tic-Tac-Toe 3x3 grid state,
evaluates win/draw conditions, and renders the retro-style console UI.
"""
import os

# Structural graphics for Tic-Tac-Toe
X_GRAPHIC = [
    r" \ / ",
    r"  X  ",
    r" / \ "
]

O_GRAPHIC = [
    r" /-\ ",
    r" | | ",
    r" \-/ "
]

EMPTY_GRAPHIC = [
    r"     ",
    r"     ",
    r"     "
]

from typing import List, Optional

class Board:
    """
    Manages the state and logic of the Tic-Tac-Toe board.
    """
    def __init__(self) -> None:
        """
        Initializes an empty 3x3 board and sets the winner to None.
        """
        # 0 to 8 representing the 3x3 grid
        self.state: List[str] = [" " for _ in range(9)]
        self.winner: Optional[str] = None

    def make_move(self, position: int, player: str) -> bool:
        """
        Attempts to place a player's marker on the board.
        
        Args:
            position (int): The 0-8 index indicating where to place the marker.
            player (str): The player's marker, either 'X' or 'O'.
            
        Returns:
            bool: True if the move was valid and placed, False otherwise.
        """
        if self.is_valid_move(position):
            self.state[position] = player
            return True
        return False

    def is_valid_move(self, position: int) -> bool:
        """
        Checks if a given position is empty and within board boundaries.
        
        Args:
            position (int): The index to check.
            
        Returns:
            bool: True if valid and empty, False otherwise.
        """
        return 0 <= position < 9 and self.state[position] == " "

    def get_available_moves(self) -> List[int]:
        """
        Retrieves a list of indices representing available squares.
        
        Returns:
            list[int]: List of available board indices.
        """
        return [i for i, cell in enumerate(self.state) if cell == " "]

    def check_winner(self) -> Optional[str]:
        """
        Evaluates the board to check if either player has met a win condition.
        
        Returns:
            str or None: The winning marker ('X' or 'O') or None if no winner yet.
        """
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
            [0, 4, 8], [2, 4, 6]             # Diagonal
        ]
        for condition in win_conditions:
            if self.state[condition[0]] != " " and \
               self.state[condition[0]] == self.state[condition[1]] == self.state[condition[2]]:
                self.winner = self.state[condition[0]]
                return self.winner
        return None

    def is_draw(self) -> bool:
        """
        Evaluates if the board is completely filled with no winner.
        
        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        return self.check_winner() is None and " " not in self.state

    def is_game_over(self) -> bool:
        """
        Determines if the game is definitively over (win or draw).
        
        Returns:
            bool: True if game over, False if game is still active.
        """
        return self.check_winner() is not None or self.is_draw()

    def display(self) -> None:
        """
        Clears the console screen and renders the board using ASCII graphics.
        """
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-"*23 + "+")
        print("|{:^23}|".format("T I C - T A C - T O E"))
        print("+" + "-"*23 + "+")
        
        for row in range(3):
            string_rows = ["", "", ""]
            for col in range(3):
                cell_index = row * 3 + col
                cell_value = self.state[cell_index]
                
                if cell_value == "X":
                    graphic = X_GRAPHIC
                elif cell_value == "O":
                    graphic = O_GRAPHIC
                else:
                    graphic = EMPTY_GRAPHIC
                    
                # Append each line of the graphic
                for i in range(3):
                    # Add a cell number to the middle of the empty cell for easy picking
                    if cell_value == " " and i == 1:
                        grid_line = f"  {cell_index + 1}  "
                    else:
                        grid_line = graphic[i]
                    
                    if col < 2:
                        string_rows[i] = string_rows[i] + grid_line + " | " # type: ignore
                    else:
                        string_rows[i] = string_rows[i] + grid_line # type: ignore
            
            for line in string_rows:
                print(f"  {line}")
                
            if row < 2:
                print(" " + "-" * 23)
        print()

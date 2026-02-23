"""
ai.py

Contains the AIPlayer class which handles decision making for the computer
opponent. Features progressive difficulty handling using Random choice, 
Blocking mechanics, and the Minimax algorithm.
"""
import random
from typing import List, Optional
from board import Board # type: ignore
import copy

class AIPlayer:
    """
    Handles calculating and executing moves for the automated opponent.
    """
    def __init__(self, difficulty: int = 1, player: str = 'O') -> None:
        """
        Initialize the AI with a specific difficulty and player marker.
        
        Args:
            difficulty (int): 1 (Easy), 2 (Medium), or 3 (Hard).
            player (str): The AI's marker, either 'X' or 'O'. Defaults to 'O'.
        """
        self.difficulty: int = difficulty
        self.player: str = player
        self.opponent: str = 'X' if player == 'O' else 'O'

    def get_move(self, board: 'Board') -> Optional[int]:
        """
        Determines the AI's next move based on the current difficulty setting.
        
        Args:
            board (Board): The current game board object.
            
        Returns:
            int or None: The index of the chosen move, or None if no moves left.
        """
        available_moves = board.get_available_moves()
        if not available_moves:
            return None
            
        if self.difficulty == 1:
            return self.get_random_move(available_moves)
        elif self.difficulty == 2:
            return self.get_medium_move(board, available_moves)
        else:
            return self.get_hard_move(board)

    def get_random_move(self, available_moves: List[int]) -> int:
        """
        Selects a random move from the list of available valid moves.
        
        Args:
            available_moves (list[int]): List of valid empty indices.
            
        Returns:
            int: A randomly selected valid index.
        """
        return random.choice(available_moves)

    def get_medium_move(self, board: 'Board', available_moves: List[int]) -> int:
        """
        A heuristic AI that tries to win if possible, block if necessary,
        and otherwise plays a random valid move.
        
        Args:
            board (Board): The game board.
            available_moves (list[int]): List of valid empty indices.
            
        Returns:
            int: The heuristically chosen index.
        """
        # 1. Try to win
        for move in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy.state[move] = self.player
            if board_copy.check_winner() == self.player:
                return move
                
        # 2. Try to block opponent's win
        for move in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy.state[move] = self.opponent
            if board_copy.check_winner() == self.opponent:
                return move
                
        # 3. Otherwise, play random
        return self.get_random_move(available_moves)

    def get_hard_move(self, board: 'Board') -> Optional[int]:
        """
        Uses the Minimax algorithm to calculate the optimal, unbeatable move.
        
        Args:
            board (Board): The game board.
            
        Returns:
            int: The optimally calculated index.
        """
        best_score = -999
        best_move = None
        available_moves = board.get_available_moves()
        
        # Introduce a tiny bit of randomness for the first move if the board is empty,
        # to prevent playing the exact same game every time
        if len(available_moves) == 9:
            return random.choice([0, 2, 4, 6, 8])

        for move in available_moves:
            board.state[move] = self.player
            score = self.minimax(board, 0, False)
            board.state[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        """
        Recursive function to calculate all possible board states and score them.
        
        Args:
            board (Board): The simulated future board state.
            depth (int): Current depth in the decision tree.
            is_maximizing (bool): Whether the current turn belongs to the AI.
            
        Returns:
            int: The calculated objective score of the outcome.
        """
        winner = board.check_winner()
        if winner == self.player:
            return 10 - depth
        elif winner == self.opponent:
            return -10 + depth
        elif board.is_draw():
            return 0

        if is_maximizing:
            best_score = -999
            for move in board.get_available_moves():
                board.state[move] = self.player
                score = self.minimax(board, depth + 1, False)
                board.state[move] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = 999
            for move in board.get_available_moves():
                board.state[move] = self.opponent
                score = self.minimax(board, depth + 1, True)
                board.state[move] = " "
                best_score = min(score, best_score)
            return best_score

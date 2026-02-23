"""
main.py

The main runner script for the project. Initializes the game states,
manages user input, and handles progression flows (play again, difficulty changes).
"""
from board import Board
from ai import AIPlayer
import time

def get_human_move(board: Board) -> int:
    """
    Prompts the human player for a terminal input and validates it.
    
    Args:
        board (Board): The current game board object.
        
    Returns:
        int: A valid, 0-indexed board position, or -1 if the player types 'q'.
    """
    while True:
        try:
            move_str = input("Enter your move (1-9) or 'q' to quit: ")
            if move_str.lower() == 'q':
                return -1
            move = int(move_str) - 1
            if board.is_valid_move(move):
                return move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")
            
    return -1 # Fallback for static analyzer

def play_game(difficulty: int, human_starts: bool) -> int:
    """
    Executes a single continuous round of Tic-Tac-Toe until win/draw/quit.
    
    Args:
        difficulty (int): The current progression level.
        human_starts (bool): Indicates if the human acts first.
        
    Returns:
        int: 1 for human win, 2 for AI win, 0 for draw, -1 if quit mid-game.
    """
    board = Board()
    human_player = 'X' if human_starts else 'O'
    ai_player = 'O' if human_starts else 'X'
    ai = AIPlayer(difficulty=difficulty, player=ai_player)
    
    current_turn: str = 'X'
    
    while not board.is_game_over():
        board.display()
        if current_turn == human_player:
            print(f"Current Difficulty Level: {difficulty}  |  You are '{human_player}'")
            move = get_human_move(board)
            if move == -1:
                return -1 # Quit
            board.make_move(move, human_player)
            current_turn = ai.player
        else:
            print(f"Current Difficulty Level: {difficulty}  |  You are '{human_player}'")
            print("AI is thinking...")
            time.sleep(0.5) # Slight pause for effect
            move = ai.get_move(board)
            if move is not None:
                board.make_move(move, ai.player)
            current_turn = human_player

    board.display()
    winner = board.check_winner()
    if winner == human_player:
        print("You win!")
        return 1
    elif winner == ai.player:
        print("AI wins!")
        return 2
    else:
        print("It's a draw!")
        return 0
        
    return -1 # Fallback for static analyzer

def main() -> None:
    """
    The master runtime loop. Manages difficulty variables and asks
    the player if they want to play another round when the game concludes.
    """
    difficulty: int = 1 # Start at easy
    human_starts: bool = True
    while True:
        result = play_game(difficulty, human_starts)
        if result == -1:
            print("Thanks for playing!")
            break
            
        # Progressive difficulty logic
        if result == 1 or result == 0:
            if difficulty < 3:
                difficulty = difficulty + 1 # type: ignore
                print("You're getting better! Increasing AI difficulty.")
                time.sleep(1.5)
        elif result == 2:
            if difficulty > 1:
                difficulty = difficulty - 1 # type: ignore
                print("AI was too strong! Decreasing difficulty.")
                time.sleep(1.5)
                
        human_starts = not human_starts
        
        print("\nPlay again? (y/n)")
        choice = input().lower()
        if choice != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

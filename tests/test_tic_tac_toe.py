import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board import Board
from ai import AIPlayer

# Board Tests
def test_board_initialization():
    b = Board()
    assert b.state == [" "] * 9
    assert b.winner is None

def test_make_valid_move():
    b = Board()
    assert b.make_move(0, "X") == True
    assert b.state[0] == "X"

def test_make_invalid_move_out_of_bounds():
    b = Board()
    assert b.make_move(9, "X") == False

def test_make_invalid_move_occupied():
    b = Board()
    b.make_move(0, "X")
    assert b.make_move(0, "O") == False
    assert b.state[0] == "X"

def test_get_available_moves():
    b = Board()
    b.make_move(0, "X")
    b.make_move(1, "O")
    assert b.get_available_moves() == [2, 3, 4, 5, 6, 7, 8]

def test_check_winner_horizontal():
    b = Board()
    b.make_move(0, "X")
    b.make_move(1, "X")
    b.make_move(2, "X")
    assert b.check_winner() == "X"
    assert b.winner == "X"

def test_check_winner_vertical():
    b = Board()
    b.make_move(1, "O")
    b.make_move(4, "O")
    b.make_move(7, "O")
    assert b.check_winner() == "O"

def test_check_winner_diagonal():
    b = Board()
    b.make_move(0, "X")
    b.make_move(4, "X")
    b.make_move(8, "X")
    assert b.check_winner() == "X"

def test_is_draw():
    b = Board()
    moves = ["X", "O", "X", 
             "X", "O", "O", 
             "O", "X", "X"]
    b.state = moves
    assert b.check_winner() is None
    assert b.is_draw() == True
    assert b.is_game_over() == True

# AI Tests
def test_ai_initialization():
    ai = AIPlayer(difficulty=2, player='O')
    assert ai.difficulty == 2
    assert ai.player == 'O'
    assert ai.opponent == 'X'

def test_ai_random_move():
    b = Board()
    ai = AIPlayer(difficulty=1)
    move = ai.get_move(b)
    assert move in range(9)

def test_ai_medium_wins_if_can():
    b = Board()
    b.make_move(0, "O")
    b.make_move(1, "O")
    ai = AIPlayer(difficulty=2, player='O')
    move = ai.get_move(b)
    # The winning move is 2
    assert move == 2

def test_ai_medium_blocks_if_must():
    b = Board()
    b.make_move(0, "X")
    b.make_move(1, "X")
    # AI should block at 2
    ai = AIPlayer(difficulty=2, player='O')
    move = ai.get_move(b)
    assert move == 2

def test_ai_hard_never_loses():
    b = Board()
    b.make_move(0, "X")
    b.make_move(4, "O")
    b.make_move(8, "X")
    # A classic trap, AI playing O
    ai = AIPlayer(difficulty=3, player='O')
    move = ai.get_move(b)
    # AI must play on an edge (1, 3, 5, 7) to avoid losing
    assert move in [1, 3, 5, 7]

def test_ai_hard_empty_board_move():
    b = Board()
    ai = AIPlayer(difficulty=3, player='O')
    move = ai.get_move(b)
    assert move in [0, 2, 4, 6, 8] # First random corner or center

def test_ai_no_moves():
    b = Board()
    b.state = ["X"] * 9
    ai = AIPlayer(difficulty=1)
    assert ai.get_move(b) is None

# Minimax tests
def test_ai_minimax():
    b = Board()
    ai = AIPlayer(difficulty=3, player='X')
    # O is about to win horizontally ([0, 1, 2])
    b.state = ["O", "O", " ", 
               "X", "X", " ", 
               " ", " ", " "]
    ai.player = 'O'
    ai.opponent = 'X'
    move = ai.get_move(b)
    assert move == 2 # O should finish the line

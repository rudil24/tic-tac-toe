import pytest
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board import Board
from ai import AIPlayer
import main

def test_board_display(capsys):
    b = Board()
    b.make_move(0, "X")
    b.make_move(1, "O")
    with patch('os.system') as mock_sys:
        b.display()
    out = capsys.readouterr().out
    assert "T I C - T A C - T O E" in out
    assert mock_sys.called

def test_ai_medium_random_fallback():
    b = Board()
    b.make_move(0, "X") # Give it something preventing immediate win/blocks
    ai = AIPlayer(difficulty=2, player='O')
    move = ai.get_move(b)
    assert move in range(9)

@patch('builtins.input', side_effect=['q'])
def test_get_human_move_quit(mock_input):
    b = Board()
    assert main.get_human_move(b) == -1

@patch('builtins.input', side_effect=['invalid', '10', '9'])
@patch('builtins.print')
def test_get_human_move_invalid_then_valid(mock_print, mock_input):
    b = Board()
    b.make_move(0, 'O') # occupy a spot to trigger different invalid move logic if needed
    assert main.get_human_move(b) == 8
    mock_print.assert_any_call("Please enter a number between 1 and 9.")
    mock_print.assert_any_call("Invalid move. Try again.")

@patch('builtins.input', side_effect=['1']) # human tries a move, but it's occupied
@patch('builtins.print')
def test_get_human_move_occupied_then_quit(mock_print, mock_input):
    b = Board()
    b.make_move(0, 'X')
    mock_input.side_effect = ['1', 'q'] # 1 is occupied
    assert main.get_human_move(b) == -1
    mock_print.assert_any_call("Invalid move. Try again.")

@patch('builtins.input', side_effect=['q'])
@patch('main.time.sleep', return_value=None)
def test_play_game_human_starts_quit(mock_sleep, mock_input, capsys):
    assert main.play_game(1, True) == -1

@patch('builtins.input', side_effect=['q'])
@patch('main.time.sleep', return_value=None)
@patch('main.AIPlayer.get_move', return_value=0)
def test_play_game_ai_starts_quit(mock_ai_move, mock_sleep, mock_input, capsys):
    assert main.play_game(1, False) == -1

@patch('builtins.input', side_effect=['y', 'n'])
@patch('main.play_game', side_effect=[1, 2]) # Win then loss
@patch('main.time.sleep', return_value=None)
def test_main_loop_progression(mock_sleep, mock_play, mock_input, capsys):
    main.main()
    out = capsys.readouterr().out
    assert "You're getting better!" in out
    assert "AI was too strong!" in out

@patch('builtins.input', side_effect=['n'])
@patch('main.play_game', side_effect=[0]) # Draw
@patch('main.time.sleep', return_value=None)
def test_main_loop_draw_progression(mock_sleep, mock_play, mock_input, capsys):
    main.main()
    out = capsys.readouterr().out
    assert "You're getting better!" in out

@patch('main.play_game', side_effect=[-1])
def test_main_loop_quit_from_game(mock_play, capsys):
    main.main()
    out = capsys.readouterr().out
    assert "Thanks for playing!" in out

# play_game winning condition paths
@patch('builtins.input', side_effect=['1'])
@patch('main.Board.is_game_over', side_effect=[False, True])
@patch('main.Board.check_winner', return_value='X')
@patch('main.time.sleep', return_value=None)
def test_play_game_human_wins(mock_sleep, mock_winner, mock_go, mock_input, capsys):
    # Human starts as 'X', makes move, then game over, wins
    assert main.play_game(1, True) == 1
    out = capsys.readouterr().out
    assert "You win!" in out

@patch('builtins.input', side_effect=['9']) 
@patch('main.Board.is_game_over', side_effect=[False, False, True])
@patch('main.Board.check_winner', return_value='X')
@patch('main.time.sleep', return_value=None)
@patch('main.AIPlayer.get_move', return_value=0)
def test_play_game_ai_wins(mock_move, mock_sleep, mock_winner, mock_go, mock_input, capsys):
    # AI starts as 'X'. Returns 0. Then human 'O' inputs 9. Game over. AI 'X' wins.
    assert main.play_game(1, False) == 2
    out = capsys.readouterr().out
    assert "AI wins!" in out

@patch('builtins.input', side_effect=['1']) 
@patch('main.Board.is_game_over', side_effect=[False, True])
@patch('main.Board.check_winner', return_value=None)
@patch('main.time.sleep', return_value=None)
def test_play_game_draw(mock_sleep, mock_winner, mock_go, mock_input, capsys):
    assert main.play_game(1, True) == 0
    out = capsys.readouterr().out
    assert "It's a draw!" in out

@patch('builtins.input', side_effect=['y', 'n'])
@patch('main.play_game', side_effect=[2, 1])
@patch('main.time.sleep', return_value=None)
def test_main_loop_no_difficulty_decrease_below_1(mock_sleep, mock_play, mock_input, capsys):
    # if difficulty is 1, a loss (2) shouldn't decrease it further
    main.main() # starts at 1, loses (stays 1), wins (increases to 2)
    # This validates the `if difficulty > 1:` branch edge cases
    out = capsys.readouterr().out
    assert "AI was too strong" not in out # because it shouldn't decrease below 1
    assert "You're getting better" in out

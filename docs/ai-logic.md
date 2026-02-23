# Tic-Tac-Toe: AI Logic Synopsis

## Overview

The Tic-Tac-Toe AI in this project was designed to be progressive, offering an "Easy" difficulty for casual play and a "Hard" difficulty that plays a mathematically perfect game. This is accomplished using a combination of randomized valid moves (for Easy) and the Minimax algorithm (for Hard).

## 1. Easy Mode (Random AI)

In Easy mode, the AI simply inspects the board for all `available_moves`. It uses Python's native `random.choice()` method to select one of the available empty indices (0-8) and returns it. This guarantees the AI plays a valid move extremely quickly without any lookahead.

## 2. Hard Mode (Minimax Algorithm)

The true core of the AI logic is the Minimax algorithm.

**The Concept:**
Minimax is a recursive algorithm used in decision theory and game theory for minimizing the possible loss for a worst-case scenario. When dealing with gains, it maximizes the minimum gain.
In Tic-Tac-Toe, the AI plays out every single possible combination of moves until the game ends (Win, Lose, or Draw).

**The Scoring:**

- If the AI wins a terminal state, it scores `+10`.
- If the Human wins a terminal state, it scores `-10`.
- If the game ends in a draw, it scores `0`.

**The Recursion (`minimax` function):**

1. **Base Case:** The function first checks if the current board state is a terminal state (someone won or it's a draw). If so, it returns the score.
2. **Maximizer (AI's Turn):** The AI loops through every empty spot, temporarily places its mark (`O`), and calls `minimax()` recursively. It wants to maximize the returned score. It undoes the move after the recursive call.
3. **Minimizer (Human's Turn):** The AI loops through every empty spot, temporarily places the opponent's mark (`X`), and calls `minimax()` recursively. It assumes the human will play perfectly and wants to minimize the score. It undoes the move after the recursive call.

**The Decision (`get_best_move` function):**
Before making a move on the *actual* board, the AI iterates through all currently available moves. For each move, it temporarily plays it and calls the `minimax` function (as the Minimizer, since it will be the human's turn next) to get the score for that branch. It selects the move that yielded the highest score and plays it.

## 3. The Implementation Flow

When `ai.get_move(board, diff)` is called from `main.py`, the AI simply checks the string `diff`.
If it equals `"easy"`, it delegates to the random choice function.
If it equals `"hard"`, it delegates to the `get_best_move` function which kicks off the Minimax calculation.

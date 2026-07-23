import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest
from game_logic import (
    new_board, get_winner, available_moves, make_move, best_ai_move, HUMAN, AI
)


def test_new_board_is_empty():
    board = new_board()
    assert len(board) == 9
    assert all(cell is None for cell in board)


def test_no_winner_on_empty_board():
    assert get_winner(new_board()) is None


@pytest.mark.parametrize("line", [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
])
def test_all_winning_lines_detected(line):
    board = [None] * 9
    for i in line:
        board[i] = "X"
    assert get_winner(board) == "X"


def test_draw_detected():
    board = ["X", "O", "X",
              "X", "O", "O",
              "O", "X", "X"]
    assert get_winner(board) == "draw"


def test_available_moves():
    board = new_board()
    assert available_moves(board) == list(range(9))
    board[0] = "X"
    assert 0 not in available_moves(board)


def test_make_move_returns_new_board_without_mutating_original():
    board = new_board()
    new = make_move(board, 4, "X")
    assert board[4] is None          
    assert new[4] == "X"


def test_make_move_rejects_occupied_cell():
    board = new_board()
    board = make_move(board, 0, "X")
    with pytest.raises(ValueError):
        make_move(board, 0, "O")


def test_make_move_rejects_out_of_range():
    board = new_board()
    with pytest.raises(ValueError):
        make_move(board, 9, "X")
    with pytest.raises(ValueError):
        make_move(board, -1, "X")


def test_ai_blocks_immediate_human_win():
    board = new_board()
    board[0] = HUMAN
    board[1] = HUMAN
    board[4] = AI
    move = best_ai_move(board, difficulty="hard")
    assert move == 2


def test_ai_takes_winning_move_when_available():
    board = new_board()
    board[0] = AI
    board[1] = AI
    board[3] = HUMAN
    board[4] = HUMAN
    move = best_ai_move(board, difficulty="hard")
    assert move == 2


def test_hard_ai_never_loses_full_game_simulation():
    board = new_board()
    player = HUMAN

    def human_move(b):
        moves = available_moves(b)
        if 4 in moves:
            return 4
        for c in (0, 2, 6, 8):
            if c in moves:
                return c
        return moves[0]

    while get_winner(board) is None:
        if player == HUMAN:
            idx = human_move(board)
        else:
            idx = best_ai_move(board, difficulty="hard")
        board = make_move(board, idx, player)
        player = AI if player == HUMAN else HUMAN

    winner = get_winner(board)
    assert winner in ("draw", AI)


def test_easy_ai_returns_a_valid_move():
    board = new_board()
    move = best_ai_move(board, difficulty="easy")
    assert move in available_moves(board)


def test_ai_move_none_when_board_full():
    board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    assert best_ai_move(board, difficulty="hard") is None

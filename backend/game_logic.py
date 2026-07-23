WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

HUMAN = "X"
AI = "O"
EMPTY = None


def new_board():
    return [EMPTY] * 9


def get_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell is not None for cell in board):
        return "draw"
    return None


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell is EMPTY]


def make_move(board, index, player):
    if index < 0 or index > 8:
        raise ValueError("Move index out of range")
    if board[index] is not None:
        raise ValueError("Cell already occupied")
    new = board[:]
    new[index] = player
    return new


def _minimax(board, player, depth=0):
    winner = get_winner(board)
    if winner == AI:
        return 10 - depth, None
    if winner == HUMAN:
        return depth - 10, None
    if winner == "draw":
        return 0, None

    moves = available_moves(board)
    best_move = moves[0]

    if player == AI:
        best_score = -float("inf")
        for m in moves:
            score, _ = _minimax(make_move(board, m, AI), HUMAN, depth + 1)
            if score > best_score:
                best_score, best_move = score, m
        return best_score, best_move
    else:
        best_score = float("inf")
        for m in moves:
            score, _ = _minimax(make_move(board, m, HUMAN), AI, depth + 1)
            if score < best_score:
                best_score, best_move = score, m
        return best_score, best_move


def best_ai_move(board, difficulty="hard"):
    import random

    moves = available_moves(board)
    if not moves:
        return None

    if difficulty == "easy":
        return random.choice(moves)

    if difficulty == "medium" and random.random() < 0.5:
        return random.choice(moves)

    _, move = _minimax(board, AI)
    return move

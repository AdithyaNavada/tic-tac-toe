from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

from game_logic import new_board, get_winner, make_move, best_ai_move, available_moves

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

GAMES = {}


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)


@app.route("/api/new_game", methods=["POST"])
def api_new_game():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default")
    difficulty = data.get("difficulty", "hard")
    GAMES[session_id] = {"board": new_board(), "difficulty": difficulty}
    return jsonify({"board": GAMES[session_id]["board"], "winner": None})


@app.route("/api/move", methods=["POST"])
def api_move():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default")
    index = data.get("index")

    if session_id not in GAMES:
        GAMES[session_id] = {"board": new_board(), "difficulty": "hard"}

    game = GAMES[session_id]
    board = game["board"]

    if index is None or not isinstance(index, int):
        return jsonify({"error": "index (int) is required"}), 400

    winner = get_winner(board)
    if winner is not None:
        return jsonify({"board": board, "winner": winner, "error": "Game already finished"}), 400

    try:
        board = make_move(board, index, "X")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    game["board"] = board
    winner = get_winner(board)

    ai_move_index = None
    if winner is None and available_moves(board):
        ai_move_index = best_ai_move(board, game["difficulty"])
        board = make_move(board, ai_move_index, "O")
        game["board"] = board
        winner = get_winner(board)

    return jsonify({
        "board": board,
        "winner": winner,
        "ai_move": ai_move_index,
    })


@app.route("/api/state", methods=["GET"])
def api_state():
    session_id = request.args.get("session_id", "default")
    game = GAMES.get(session_id)
    if not game:
        return jsonify({"board": new_board(), "winner": None})
    return jsonify({"board": game["board"], "winner": get_winner(game["board"])})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)

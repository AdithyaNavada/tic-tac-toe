# Tic Tac Toe

A full-stack Tic Tac Toe web app with a Python Flask backend and a plain HTML/CSS/JavaScript frontend. Supports two game modes — Player vs Player and Player vs Computer — with three AI difficulty levels powered by the Minimax algorithm.

🔗 **Live Demo:** [https://tic-tac-toe-e7wa.onrender.com](https://tic-tac-toe-e7wa.onrender.com)  

---

## Features

- Welcome screen with animated grid drawing
- Mode selection — You & a Friend (local 2-player) or You vs Computer
- Three AI difficulty levels — Easy (random), Medium (mixed), Hard (unbeatable Minimax)
- Animated X and O marks drawn with SVG
- Win detection with cell highlighting
- Score tracking across rounds
- Reset and Play Again without leaving the game

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3, Flask, flask-cors |
| Frontend   | HTML, CSS, Vanilla JavaScript       |
| AI Logic   | Minimax algorithm (Python)          |
| Testing    | pytest, Selenium            |
| Deployment | Render                              |

---

## Project Structure

```
tic-tac-toe/
├── backend/
│   ├── app.py              # Flask app — routes, session management, serves frontend
│   ├── game_logic.py       # Board logic, win detection, Minimax AI
│   └── requirements.txt    # Flask, flask-cors, gunicorn
├── frontend/
│   ├── index.html          # Single-page app — welcome, mode select, game screens
│   ├── app.js              # All game state and UI logic (vanilla JS)
│   ├── style.css           # Full styling — animations, responsive layout
│   ├── manifest.json       # PWA manifest
│   └── service-worker.js   # Offline support
├── tests/
│   ├── unit/
│   │   └── test_game_logic.py      # pytest unit tests for game_logic.py
│   ├── e2e_selenium/
│   │   └── test_web.py             # Selenium E2E tests (desktop browser)
│   ├── e2e_appium/
│   │   └── test_mobile.py          # Appium E2E tests (Android mobile browser)
│   └── requirements-test.txt       # pytest, selenium, webdriver-manager, appium
└── .gitignore
```

---

## Getting Started (Run Locally)

### Prerequisites

- Python 3.10+
- Chrome browser

### 1. Clone the repo

```bash
git clone https://github.com/AdithyaNavada/tic-tac-toe.git
cd tic-tac-toe
```

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the server

```bash
python app.py
```

The app serves both the API and the frontend. Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## API Endpoints

| Method | Endpoint          | Description                                      |
|--------|-------------------|--------------------------------------------------|
| POST   | `/api/new_game`   | Start a new game session with chosen difficulty  |
| POST   | `/api/move`       | Submit player move, get board + AI response      |
| GET    | `/api/state`      | Get current board state for a session            |

**Request body for `/api/move`:**
```json
{
  "session_id": "session-abc123",
  "index": 4
}
```

**Response:**
```json
{
  "board": ["X", null, null, null, "O", null, null, null, null],
  "winner": null,
  "ai_move": 4
}
```

---

## AI — Minimax Algorithm

The Hard difficulty uses the **Minimax algorithm** — it evaluates every possible future game state and always picks the optimal move. The computer never loses on Hard mode. The best a human can do is draw.

- **Easy** — picks a random available move  
- **Medium** — 50% chance of random move, 50% Minimax  
- **Hard** — full Minimax, unbeatable  

---

## Running Tests

### Install test dependencies

```bash
cd tests
pip install -r requirements-test.txt
```

### Unit Tests

Tests the core game logic — board creation, win detection, draw detection, make_move validation, and Minimax AI behaviour.

```bash
pytest tests/unit/ -v
```

**What's tested:**
- Empty board initialisation
- All 8 winning line combinations
- Draw detection
- Move validation (occupied cell, out of range)
- AI blocks human winning move
- AI takes its own winning move
- Hard AI never loses in a full simulated game
- Easy AI returns a valid move
- AI returns None when board is full

### Selenium E2E Tests (browser)

Tests the full user flow in a real Chrome browser against the running server.

```bash
# Make sure the Flask server is running first
python backend/app.py

# Then in another terminal:
pytest tests/e2e_selenium/ -v
```

**What's tested:**
- Welcome screen loads correctly
- Full friend vs friend game plays to a win with winning cells highlighted
- vs Computer (Easy) game completes with valid result
- Reset button clears the board
- Full walkthrough — all 3 difficulty modes in one test


## Test Coverage Summary

| Layer       | Tool      | Tests | What it covers                                      |
|-------------|-----------|-------|-----------------------------------------------------|
| Unit        | pytest    | 11    | Game logic, AI, edge cases, validation              |
| E2E Browser | Selenium  | 5     | Welcome → mode select → gameplay → win/draw → reset |

---

## Author

**Adithya P Navada**  
[GitHub](https://github.com/AdithyaNavada) · [LinkedIn](https://www.linkedin.com/in/adithya-p-navada/)

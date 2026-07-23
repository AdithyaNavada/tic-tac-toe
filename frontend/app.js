const API_BASE = "";
const SESSION_ID = "session-" + Math.random().toString(36).slice(2);

let mode = null;          // 'friend' | 'computer'
let difficulty = "hard";  // 'easy' | 'medium' | 'hard'
let board = Array(9).fill(null);
let currentPlayer = "X";
let gameOver = false;
let scores = { X: 0, O: 0, draw: 0 };

const screens = {
  welcome: document.getElementById("screen-welcome"),
  mode: document.getElementById("screen-mode"),
  game: document.getElementById("screen-game"),
};
const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status-line");
const gameModeLabel = document.getElementById("game-mode-label");
const difficultyPicker = document.getElementById("difficulty-picker");
const scoreXEl = document.getElementById("score-x");
const scoreOEl = document.getElementById("score-o");
const scoreDrawEl = document.getElementById("score-draw");
const labelX = document.getElementById("label-x");
const labelO = document.getElementById("label-o");
const btnPlayAgain = document.getElementById("btn-play-again");

function showScreen(name) {
  Object.values(screens).forEach((s) => s.classList.remove("active"));
  screens[name].classList.add("active");
}

const friendCard = document.getElementById("btn-vs-friend");
const computerCard = document.getElementById("btn-vs-computer");
const modeHint = document.getElementById("mode-hint");
const TRANSITION_MS = 620; // pause between the card animation and opening the game

let modeTransitioning = false;

function resetModeScreen() {
  modeTransitioning = false;
  mode = null;
  friendCard.classList.remove("chosen", "dismiss", "exit-down");
  computerCard.classList.remove("chosen", "dismiss", "exit-down");
  difficultyPicker.classList.add("hidden");
  difficultyPicker.classList.remove("reveal");
  document.querySelectorAll(".chip").forEach((c) => c.classList.remove("selected"));
  if (modeHint) modeHint.textContent = "How do you want to play?";
}

document.getElementById("btn-enter").addEventListener("click", () => {
  resetModeScreen();
  showScreen("mode");
});

document.getElementById("mode-back").addEventListener("click", () => {
  // If the difficulty picker is showing, step back to the two cards first.
  if (mode === "computer" && !modeTransitioning) {
    resetModeScreen();
    return;
  }
  showScreen("welcome");
});

document.getElementById("game-back").addEventListener("click", () => {
  resetModeScreen();
  showScreen("mode");
});

// You & a Friend: card glides to the middle, then the game opens shortly after.
friendCard.addEventListener("click", () => {
  if (modeTransitioning) return;
  modeTransitioning = true;
  mode = "friend";
  if (modeHint) modeHint.textContent = "Starting a local match…";
  difficultyPicker.classList.add("hidden");
  difficultyPicker.classList.remove("reveal");
  computerCard.classList.add("dismiss");
  friendCard.classList.add("chosen");
  setTimeout(startGame, TRANSITION_MS);
});

// You vs Computer: friend card drops away, this card takes over and reveals difficulty.
computerCard.addEventListener("click", () => {
  if (modeTransitioning || mode === "computer") return;
  mode = "computer";
  if (modeHint) modeHint.textContent = "Pick your challenge";
  friendCard.classList.add("exit-down");
  computerCard.classList.add("chosen");
  difficultyPicker.classList.remove("hidden");
  requestAnimationFrame(() =>
    requestAnimationFrame(() => difficultyPicker.classList.add("reveal"))
  );
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    if (modeTransitioning) return;
    modeTransitioning = true;
    document.querySelectorAll(".chip").forEach((c) => c.classList.remove("selected"));
    chip.classList.add("selected");
    difficulty = chip.dataset.difficulty;
    setTimeout(startGame, TRANSITION_MS);
  });
});

document.getElementById("game-reset").addEventListener("click", resetBoard);
btnPlayAgain.addEventListener("click", resetBoard);

function startGame() {
  gameModeLabel.textContent = mode === "friend" ? "You & a Friend" : `You vs Computer (${difficulty})`;
  labelX.textContent = mode === "friend" ? "X" : "You";
  labelO.textContent = mode === "friend" ? "O" : "CPU";
  showScreen("game");
  resetBoard();
}

async function resetBoard() {
  board = Array(9).fill(null);
  currentPlayer = "X";
  gameOver = false;
  btnPlayAgain.classList.add("hidden");
  renderBoard();
  setStatus(`${mode === "friend" ? "X's" : "Your"} turn`);

  if (mode === "computer") {
    try {
      await fetch(`${API_BASE}/api/new_game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: SESSION_ID, difficulty }),
      });
    } catch (e) {
      console.error("Failed to start new game on server", e);
    }
  }
}

function renderBoard() {
  boardEl.innerHTML = "";
  board.forEach((val, i) => {
    const cell = document.createElement("button");
    cell.className = "cell" + (val ? ` filled ${val.toLowerCase()}` : "");
    cell.dataset.index = i;
    cell.dataset.testid = `cell-${i}`;
    cell.setAttribute("aria-label", `Cell ${i + 1}${val ? `, ${val}` : ", empty"}`);
    if (val === "X") cell.innerHTML = markSVG("x");
    if (val === "O") cell.innerHTML = markSVG("o");
    cell.addEventListener("click", () => handleCellClick(i));
    boardEl.appendChild(cell);
  });
}

function markSVG(type) {
  if (type === "x") {
    return `<svg viewBox="0 0 100 100"><path class="mark-path" d="M22 22 L78 78" /><path class="mark-path" d="M78 22 L22 78" /></svg>`;
  }
  return `<svg viewBox="0 0 100 100"><circle class="mark-path" cx="50" cy="50" r="34" /></svg>`;
}

function setStatus(text) {
  statusEl.textContent = text;
}

const WIN_LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6],
];

function getWinner(b) {
  for (const [a, c, d] of WIN_LINES) {
    if (b[a] && b[a] === b[c] && b[a] === b[d]) return { winner: b[a], line: [a, c, d] };
  }
  if (b.every((cell) => cell !== null)) return { winner: "draw", line: [] };
  return { winner: null, line: [] };
}

function highlightWin(line) {
  line.forEach((i) => {
    boardEl.children[i].classList.add("win");
  });
}

function endGame(winner, line) {
  gameOver = true;
  if (winner === "draw") {
    scores.draw++;
    setStatus("It's a draw!");
  } else {
    scores[winner]++;
    highlightWin(line);
    if (mode === "friend") {
      setStatus(`${winner} wins! 🎉`);
    } else {
      setStatus(winner === "X" ? "You win! 🎉" : "Computer wins.");
    }
  }
  scoreXEl.textContent = scores.X;
  scoreOEl.textContent = scores.O;
  scoreDrawEl.textContent = scores.draw;
  btnPlayAgain.classList.remove("hidden");
}

function handleCellClick(index) {
  if (gameOver || board[index] !== null) return;

  if (mode === "friend") {
    playLocalMove(index);
  } else {
    playAgainstComputer(index);
  }
}

function playLocalMove(index) {
  board[index] = currentPlayer;
  renderBoard();
  const { winner, line } = getWinner(board);
  if (winner) {
    endGame(winner, line);
    return;
  }
  currentPlayer = currentPlayer === "X" ? "O" : "X";
  setStatus(`${currentPlayer}'s turn`);
}

async function playAgainstComputer(index) {
  board[index] = "X";
  renderBoard();
  setStatus("Computer is thinking...");

  try {
    const res = await fetch(`${API_BASE}/api/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: SESSION_ID, index }),
    });
    const data = await res.json();

    if (data.error) {
      setStatus(data.error);
      return;
    }

    board = data.board;
    renderBoard();

    if (data.winner) {
      const { line } = getWinner(board);
      endGame(data.winner, line);
    } else {
      setStatus("Your turn");
    }
  } catch (e) {
    console.error(e);
    setStatus("Couldn't reach the server. Check your connection.");
  }
}

renderBoard();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("service-worker.js").catch(() => {});
  });
}
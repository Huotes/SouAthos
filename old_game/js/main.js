// js/main.js
import { initGame, startGridResizeLoop } from "./core/init.js";
import { gameState } from "./core/state.js";
import { draw } from "./render/render.js";
import { createParticles } from "./utils/utils.js";

const API_BASE = "/api";

// ===============================
// LocalStorage & Backend
// ===============================
export function setPlayerName(name) {
  localStorage.setItem("souAthos_playerName", name.toUpperCase().slice(0, 5));
}

export function getPlayerName() {
  return localStorage.getItem("souAthos_playerName") || "";
}

export async function fetchLeaderboard() {
  try {
    const res = await fetch(`${API_BASE}/scores`);
    if (!res.ok) throw new Error("Falha ao buscar leaderboard");
    const data = await res.json();
    import("./ui/scoreUI.js").then((mod) =>
      mod.scoreUI.renderLeaderboard(data)
    );
  } catch (err) {
    console.error(err);
    const container = document.getElementById("leaderboard-list");
    if (container) {
      container.innerHTML = `<div style="text-align:center;color:#f88">Erro</div>`;
    }
  }
}

export async function postScoreIfHigh(name, score) {
  if (!name || name.length === 0) return;

  try {
    await fetch(`${API_BASE}/score`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: name.slice(0, 5).toUpperCase(),
        score: Math.max(0, Math.floor(score)),
      }),
    });
    await fetchLeaderboard();
  } catch (err) {
    console.error("Erro ao postar score:", err);
  }
}

// ===============================
// UI Elements
// ===============================
const uiElements = {
  playerModal: document.getElementById("player-modal"),
  playerNameInput: document.getElementById("player-name"),
  startBtn: document.getElementById("start-btn"),
  restartBtn: document.getElementById("restart-btn"),
};

// ===============================
// Modal e inicialização do jogo
// ===============================
window.addEventListener("load", () => {
  uiElements.playerModal.style.display = "flex";

  // Inicializa partículas do fundo animado (fora do canvas do game)
  createParticles();

  // Leaderboard
  fetchLeaderboard();
  setInterval(fetchLeaderboard, 6000); // atualiza leaderboard a cada 6s
});

uiElements.startBtn.addEventListener("click", () => {
  const name = uiElements.playerNameInput.value.trim().toUpperCase();
  if (!name) return alert("Digite um nome válido!");
  setPlayerName(name);

  uiElements.playerModal.style.display = "none";
  initGame();
  startGridResizeLoop();
});

uiElements.restartBtn.addEventListener("click", () => {
  initGame();
});

// ===============================
// Controles via teclado
// ===============================
window.addEventListener("keydown", (e) => {
  const directions = {
    ArrowUp: "up",
    ArrowDown: "down",
    ArrowLeft: "left",
    ArrowRight: "right",
    w: "up",
    s: "down",
    a: "left",
    d: "right",
  };

  const dir = directions[e.key];
  if (!dir) return;

  if (
    (dir === "up" && gameState.direction !== "down") ||
    (dir === "down" && gameState.direction !== "up") ||
    (dir === "left" && gameState.direction !== "right") ||
    (dir === "right" && gameState.direction !== "left")
  ) {
    gameState.nextDirection = dir;
  }
});


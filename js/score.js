// score.js - gerencia nome do jogador, leaderboard e envio de score ao backend

const API_BASE = "/api";

function setPlayerName(name) {
  localStorage.setItem("souAthos_playerName", name.toUpperCase().slice(0,5));
  updatePlayerNameUI();
}

function getPlayerName() {
  return localStorage.getItem("souAthos_playerName") || "";
}

function updatePlayerNameUI() {
  const name = getPlayerName();
  const input = document.getElementById("player-name");
  const modal = document.getElementById("player-modal");
  if (input) input.value = name;
  // esconder modal se nome válido
  if (name && name.length > 0) {
    if (modal) modal.style.display = "none";
    // mostrar nome na UI de pontuação (à esquerda)
    const scoreContainer = document.querySelector(".score-container");
    if (scoreContainer && !document.getElementById("player-display")) {
      const el = document.createElement("div");
      el.id = "player-display";
      el.style.fontSize = "0.9em";
      el.style.marginLeft = "10px";
      el.textContent = `Jogador: ${name}`;
      scoreContainer.appendChild(el);
    } else if (document.getElementById("player-display")) {
      document.getElementById("player-display").textContent = `Jogador: ${name}`;
    }
  } else {
    if (modal) modal.style.display = "flex";
  }
}

async function fetchLeaderboard() {
  try {
    const res = await fetch(`${API_BASE}/scores`);
    if (!res.ok) throw new Error("Falha ao buscar leaderboard");
    const data = await res.json();
    renderLeaderboard(data);
  } catch (err) {
    console.error(err);
    const container = document.getElementById("leaderboard-list");
    if (container) container.innerHTML = `<div style="text-align:center;color:#f88">Erro</div>`;
  }
}

function renderLeaderboard(items) {
  const container = document.getElementById("leaderboard-list");
  if (!container) return;
  if (!items || items.length === 0) {
    container.innerHTML = `<div style="text-align:center;color:#aaa">Sem registros</div>`;
    return;
  }
  const top = items.slice(0, 8); // mostrar top 8
  container.innerHTML = "";
  top.forEach((it, idx) => {
    const row = document.createElement("div");
    row.style.display = "flex";
    row.style.justifyContent = "space-between";
    row.style.marginBottom = "6px";
    row.innerHTML = `<span style="opacity:0.9">${idx+1}. ${it.name}</span><span style="font-weight:700">${it.score}</span>`;
    container.appendChild(row);
  });
}

async function postScoreIfHigh(name, score) {
  if (!name || name.length === 0) return;
  // enviar POST simples; backend só guarda se for maior que o anterior
  try {
    await fetch(`${API_BASE}/score`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name.slice(0,5).toUpperCase(), score: Math.max(0, Math.floor(score)) })
    });
    // atualizar leaderboard localmente depois de salvar
    await fetchLeaderboard();
  } catch (err) {
    console.error("Erro ao postar score:", err);
  }
}

// evento do modal
window.addEventListener("load", () => {
  const startBtn = document.getElementById("start-btn");
  const input = document.getElementById("player-name");
  updatePlayerNameUI();
  fetchLeaderboard();
  // atualizar leaderboard a cada 6s
  setInterval(fetchLeaderboard, 6000);

  if (startBtn) {
    startBtn.addEventListener("click", () => {
      const v = (input && input.value) ? input.value.trim().toUpperCase().slice(0,5) : "";
      if (!v || v.length === 0) {
        alert("Digite um nome (max 5 caracteres).");
        return;
      }
      if (v.length > 5) {
        alert("Nome deve ter no máximo 5 caracteres.");
        return;
      }
      setPlayerName(v);
      // dispara inicialização do jogo caso exista função global initGame
      if (typeof initGame === "function") {
        initGame();
      }
    });
  }
});

// expose functions for game.js to call
window.souAthosScore = {
  getPlayerName,
  postScoreIfHigh,
  fetchLeaderboard
};


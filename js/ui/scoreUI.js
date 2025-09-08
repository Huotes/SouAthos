// ui/scoreUI.js
import { getPlayerName, setPlayerName, fetchLeaderboard } from "../main.js";

export const scoreUI = {
  updatePlayerNameUI: function() {
    const name = getPlayerName();
    const input = document.getElementById("player-name");
    const modal = document.getElementById("player-modal");
    if (input) input.value = name;

    if (name && name.length > 0) {
      if (modal) modal.style.display = "none";

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
  },

  renderLeaderboard: function(items) {
    const container = document.getElementById("leaderboard-list");
    if (!container) return;
    if (!items || items.length === 0) {
      container.innerHTML = `<div style="text-align:center;color:#aaa">Sem registros</div>`;
      return;
    }
    const top = items.slice(0, 8);
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
};

// Inicialização do modal e botão
window.addEventListener("load", () => {
  scoreUI.updatePlayerNameUI();
  fetchLeaderboard(); // atualiza leaderboard ao abrir
  setInterval(fetchLeaderboard, 6000);
});


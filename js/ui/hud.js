// ui/hud.js
import { gameState } from "../core/state.js";
import { uiElements } from "./elements.js";

// Atualiza o placar
export function updateScore() {
  if (uiElements.score) uiElements.score.textContent = `Score: ${gameState.score}`;
  if (uiElements.highScore) uiElements.highScore.textContent = `High: ${gameState.highScore}`;
}

// Atualiza o nível
export function updateLevel() {
  if (uiElements.level) uiElements.level.textContent = `Nível: ${gameState.level}`;
}

// Mostra conquista animada
export function showAchievement(text) {
  if (!uiElements.achievement || !uiElements.achievementText) return;
  uiElements.achievementText.textContent = text;
  uiElements.achievement.classList.add("show");

  setTimeout(() => {
    uiElements.achievement.classList.remove("show");
  }, 3000);
}


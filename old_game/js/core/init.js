import { gameState, gridResizeConfig } from "./state.js";
import { generateFood, gameUpdate, resizeGridDynamically } from "./engine.js";
import { updateScore, updateLevel } from "../ui/hud.js";
import { uiElements } from "../ui/elements.js";

// ==============================
// Inicializa o jogo
// ==============================
export function initGame() {
  gameState.snake = [
    { x: 5, y: 10 },
    { x: 4, y: 10 },
    { x: 3, y: 10 },
  ];
  generateFood();
  gameState.score = 0;
  gameState.level = 1;
  gameState.direction = "right";
  gameState.nextDirection = "right";
  gameState.gameSpeed = 130;

  updateScore();
  updateLevel();

  if (gameState.gameLoop) clearInterval(gameState.gameLoop);
  gameState.gameLoop = setInterval(gameUpdate, gameState.gameSpeed);

  uiElements.gameOver.style.display = "none";
  document.body.className = "color-theme-1";
  gameState.colorTheme = 1;
}

// ==============================
// Loop para redimensionar a grade
// ==============================
export function startGridResizeLoop() {
  setInterval(resizeGridDynamically, gridResizeConfig.interval);
}


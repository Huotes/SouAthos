// core/engine.js
import { gameState, gridResizeConfig } from "./state.js";
import { uiElements } from "../ui/elements.js";
import { updateScore, updateLevel } from "../ui/hud.js";
import { draw, animateFoodSwap, canvas, gridSize } from "../render/render.js";
import { randomInt, isPositionOccupied, shakeScreen, changeColorTheme, showAchievement } from "../utils/utils.js";
import { getPlayerName, postScoreIfHigh } from "../main.js";
import { flashCanvasBorder } from "../utils/utils.js";
import { playResizeIndicator } from "../utils/utils.js";
import { createParticles } from "../utils/utils.js";

// ==============================
// Gera comida em posição livre
// ==============================
export function generateFood() {
  const food = {
    x: Math.floor(Math.random() * (canvas.width / gridSize)),
    y: Math.floor(Math.random() * (canvas.height / gridSize)),
    special: Math.random() < 0.1,
    cheater: Math.random() < 0.125,
  };

  if (isPositionOccupied(food.x, food.y, gameState.snake)) {
    return generateFood();
  }
  gameState.food = food;
}

// ==============================
// Cobra come a comida
// ==============================
export function eatFood() {
  const points = gameState.food.special ? 5 : 1;
  gameState.score += points;

  if (gameState.score > gameState.highScore) {
    gameState.highScore = gameState.score;
    localStorage.setItem("snakeHighScore", gameState.highScore);
  }
  updateScore();

  const newLevel = Math.floor(gameState.score / 5) + 1;
  if (newLevel > gameState.level) {
  gameState.level = newLevel;
  updateLevel();

  gameState.gameSpeed = Math.max(50, 130 - (gameState.level - 1) * 15);
  clearInterval(gameState.gameLoop);
  gameState.gameLoop = setInterval(gameUpdate, gameState.gameSpeed);

  gameState.colorTheme = changeColorTheme();
  showAchievement(`Nível ${gameState.level} alcançado!`);

  // --- Só borda e partículas ---
  flashCanvasBorder();
  const themeColor = getComputedStyle(document.body).getPropertyValue("--snake-color") || "#0ff";
  createParticles(30, themeColor);
  }

  // dentro de eatFood(), logo após updateScore():
  if (gameState.score % 10 === 0) {
    flashCanvasBorder();
  }

  generateFood(); // comida reaparece
}

// ==============================
// Redimensiona a grade dinamicamente
// ==============================
export function resizeGridDynamically() {
  const newWidth = randomInt(gridResizeConfig.minWidth, gridResizeConfig.maxWidth);
  const newHeight = randomInt(gridResizeConfig.minHeight, gridResizeConfig.maxHeight);

  const newCols = Math.floor(newWidth / gridSize);
  const newRows = Math.floor(newHeight / gridSize);

  gameState.snake = gameState.snake.map((seg) => ({
    x: Math.min(seg.x, newCols - 1),
    y: Math.min(seg.y, newRows - 1),
  }));

  if (gameState.food.x >= newCols) gameState.food.x = newCols - 1;
  if (gameState.food.y >= newRows) gameState.food.y = newRows - 1;

  canvas.width = newCols * gridSize;
  canvas.height = newRows * gridSize;

  canvas.style.transition = "width 1s, height 1s";
  canvas.style.width = canvas.width + "px";
  canvas.style.height = canvas.height + "px";
}

// ==============================
// Game Over consolidado
// ==============================
function gameOver() {
  clearInterval(gameState.gameLoop);

  const player = getPlayerName();
  postScoreIfHigh(player, gameState.score);

  if (uiElements.finalScore) uiElements.finalScore.textContent = gameState.score;
  if (uiElements.finalLevel) uiElements.finalLevel.textContent = gameState.level;
  if (uiElements.gameOver) uiElements.gameOver.style.display = "flex";
}

// ==============================
// Loop principal do jogo
// ==============================
export function gameUpdate() {
  const head = { ...gameState.snake[0] };
  switch (gameState.nextDirection) {
    case "up": head.y--; break;
    case "down": head.y++; break;
    case "left": head.x--; break;
    case "right": head.x++; break;
  }
  gameState.direction = gameState.nextDirection;

  const cols = canvas.width / gridSize;
  const rows = canvas.height / gridSize;
  if (head.x < 0 || head.x >= cols || head.y < 0 || head.y >= rows) {
    shakeScreen();
    gameOver();
    return;
  }

  if (isPositionOccupied(head.x, head.y, gameState.snake)) {
    shakeScreen();
    gameOver();
    return;
  }

  gameState.snake.unshift(head);

  if (head.x === gameState.food.x && head.y === gameState.food.y) {
    if (gameState.food.cheater) {
      const dirs = [{x:1,y:0},{x:-1,y:0},{x:0,y:1},{x:0,y:-1}];
      const valid = dirs.map(d=>({x:gameState.food.x+d.x,y:gameState.food.y+d.y}))
        .filter(p=>p.x>=0 && p.x<cols && p.y>=0 && p.y<rows && !isPositionOccupied(p.x,p.y,gameState.snake));

      if(valid.length>0){
        const choice = valid[Math.floor(Math.random()*valid.length)];
        const oldX = gameState.food.x, oldY = gameState.food.y;
        gameState.food.x = choice.x; gameState.food.y = choice.y;
        gameState.food.cheater = false;
        animateFoodSwap(oldX, oldY, choice.x, choice.y);
        gameState.snake.pop();
      } else eatFood();
    } else eatFood();
  } else gameState.snake.pop();

  draw(gameState.snake, gameState.food);
}

function resizeGameCanvas() {
  const canvas = document.getElementById("game-canvas");
  if (!canvas) return;

  const parent = canvas.parentElement;
  const size = Math.min(parent.clientWidth, parent.clientHeight);

  canvas.width = size;
  canvas.height = size;
}

// Novo handler de resize com indicador
function handleResize() {
  playResizeIndicator(() => {
    resizeGameCanvas();
  });
}

window.addEventListener("resize", handleResize);
window.addEventListener("load", resizeGameCanvas);


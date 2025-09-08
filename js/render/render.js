// render/render.js
import { gameState } from "../core/state.js";
import { easeInOutQuad, oscillatingColor, particles, updateParticles } from "../utils/utils.js";

// Configurações do canvas
export const canvas = document.getElementById("game-canvas");
export const ctx = canvas.getContext("2d");
export const gridSize = 20;

// ===============================
// Helper para pegar variáveis CSS
// ===============================
function cssVar(name, fallback) {
  const v = getComputedStyle(document.body).getPropertyValue(name).trim();
  return v || fallback;
}

// ===============================
// Função principal de renderização
// ===============================
export function draw(snake, food) {
  // Limpar o canvas
  ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Desenhar elementos do jogo
  drawGrid();
  drawSnake(snake);
  drawFood(food);

  // Atualiza partículas internas do canvas
  updateParticles(ctx);
}

// ===============================
// Desenho da grade
// ===============================
function drawGrid() {
  ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
  ctx.lineWidth = 0.5;

  for (let x = 0; x < canvas.width; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }

  for (let y = 0; y < canvas.height; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
}

// ===============================
// Desenho da cobra
// ===============================
function drawSnake(snake) {
  snake.forEach((segment, index) => {
    if (index === 0) {
      // Cabeça
      ctx.fillStyle = cssVar("--snake-color", "#0ff");
      ctx.shadowBlur = 15;
      ctx.shadowColor = ctx.fillStyle;
    } else {
      // Corpo com gradiente
      const gradient = ctx.createLinearGradient(
        segment.x * gridSize,
        segment.y * gridSize,
        segment.x * gridSize + gridSize,
        segment.y * gridSize + gridSize
      );
      gradient.addColorStop(0, cssVar("--snake-color", "#0ff"));
      gradient.addColorStop(1, "#00ff9d");

      ctx.fillStyle = gradient;
      ctx.shadowBlur = 10;
      ctx.shadowColor = cssVar("--snake-color", "#0ff");
    }

    if (ctx.roundRect) {
      ctx.beginPath();
      ctx.roundRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize, 5);
      ctx.fill();
    } else {
      ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
    }

    if (index === 0) drawSnakeEyes(segment);
  });

  ctx.shadowBlur = 0;
}

// ===============================
// Olhos da cobra
// ===============================
function drawSnakeEyes(head) {
  ctx.fillStyle = "#000";
  let eye1X, eye1Y, eye2X, eye2Y;

  switch (gameState.direction) {
    case "up":
      eye1X = head.x * gridSize + 5;
      eye1Y = head.y * gridSize + 5;
      eye2X = head.x * gridSize + gridSize - 9;
      eye2Y = head.y * gridSize + 5;
      break;
    case "down":
      eye1X = head.x * gridSize + 5;
      eye1Y = head.y * gridSize + gridSize - 9;
      eye2X = head.x * gridSize + gridSize - 9;
      eye2Y = head.y * gridSize + gridSize - 9;
      break;
    case "left":
      eye1X = head.x * gridSize + 5;
      eye1Y = head.y * gridSize + 5;
      eye2X = head.x * gridSize + 5;
      eye2Y = head.y * gridSize + gridSize - 9;
      break;
    case "right":
      eye1X = head.x * gridSize + gridSize - 9;
      eye1Y = head.y * gridSize + 5;
      eye2X = head.x * gridSize + gridSize - 9;
      eye2Y = head.y * gridSize + gridSize - 9;
      break;
  }

  ctx.beginPath();
  ctx.arc(eye1X, eye1Y, 3, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(eye2X, eye2Y, 3, 0, Math.PI * 2);
  ctx.fill();
}

// ===============================
// Desenho da comida
// ===============================
function drawFood(food) {
  const normalColor  = cssVar("--food-color", "#ffea00");
  const specialColor = cssVar("--food-special-color", "#a86bff");

  if (food.cheater) {
    const oscColor = oscillatingColor("#ff4444", "#ffff00", 0.01);
    ctx.fillStyle = oscColor;
    ctx.shadowBlur = 25;
    ctx.shadowColor = oscColor;
    ctx.beginPath();
    ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI*2);
    ctx.fill();
    ctx.shadowBlur = 0;
    return;
  }

  if (food.special) {
    ctx.fillStyle = specialColor;
    ctx.shadowBlur = 20;
    ctx.shadowColor = ctx.fillStyle;

    ctx.beginPath();
    ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2, 0, Math.PI*2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2 + 3, 0, Math.PI*2);
    ctx.strokeStyle = ctx.fillStyle;
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.shadowBlur = 0;
    return;
  }

  ctx.fillStyle = normalColor;
  ctx.shadowBlur = 15;
  ctx.shadowColor = ctx.fillStyle;
  ctx.beginPath();
  ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI*2);
  ctx.fill();
  ctx.shadowBlur = 0;
}

// ===============================
// Animação da comida “fugindo”
// ===============================
export function animateFoodSwap(oldX, oldY, newX, newY) {
  let progress = 0;
  const steps = 15;
  const interval = setInterval(() => {
    progress++;
    const t = progress / steps;
    const eased = easeInOutQuad(t);

    const interpX = oldX * gridSize + (newX - oldX) * gridSize * eased;
    const interpY = oldY * gridSize + (newY - oldY) * gridSize * eased;

    ctx.fillStyle = "rgba(0,0,0,0.7)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    drawGrid();
    drawSnake(gameState.snake);

    ctx.fillStyle = cssVar("--food-color", "#ffea00");
    ctx.shadowBlur = 15;
    ctx.shadowColor = ctx.fillStyle;
    ctx.beginPath();
    ctx.arc(interpX + gridSize/2, interpY + gridSize/2, gridSize/2 - 2, 0, Math.PI*2);
    ctx.fill();
    ctx.shadowBlur = 0;

    if (progress >= steps) clearInterval(interval);
  }, 16);
}


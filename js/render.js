// Funções de renderização do jogo

// Configurações do canvas
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const gridSize = 20;

// Desenhar o jogo
function draw(snake, food) {
  // Limpar o canvas
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Desenhar a grade
  drawGrid();

  // Desenhar a cobra
  drawSnake(snake);

  // Desenhar a comida
  drawFood(food);
}

// Desenhar a grade do jogo
function drawGrid() {
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
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

// Desenhar a cobra
function drawSnake(snake) {
  snake.forEach((segment, index) => {
    if (index === 0) {
      // Cabeça
      ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--snake-color');
      ctx.shadowBlur = 15;
      ctx.shadowColor = getComputedStyle(document.body).getPropertyValue('--snake-color');
    } else {
      // Corpo com gradiente
      const gradient = ctx.createLinearGradient(
        segment.x * gridSize, segment.y * gridSize,
        segment.x * gridSize + gridSize, segment.y * gridSize + gridSize
      );
      gradient.addColorStop(0, getComputedStyle(document.body).getPropertyValue('--snake-color'));
      gradient.addColorStop(1, '#00ff9d');
      ctx.fillStyle = gradient;
      ctx.shadowBlur = 10;
      ctx.shadowColor = getComputedStyle(document.body).getPropertyValue('--snake-color');
    }

    if (ctx.roundRect) {
      ctx.beginPath();
      ctx.roundRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize, 5);
      ctx.fill();
    } else {
      ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
    }

    if (index === 0) {
      drawSnakeEyes(segment);
    }
  });
  ctx.shadowBlur = 0;
}

// Desenhar os olhos da cobra
function drawSnakeEyes(head) {
  ctx.fillStyle = '#000';
  let eye1X, eye1Y, eye2X, eye2Y;
  switch(gameState.direction) {
    case 'up':
      eye1X = head.x * gridSize + 5;
      eye1Y = head.y * gridSize + 5;
      eye2X = head.x * gridSize + gridSize - 9;
      eye2Y = head.y * gridSize + 5;
      break;
    case 'down':
      eye1X = head.x * gridSize + 5;
      eye1Y = head.y * gridSize + gridSize - 9;
      eye2X = head.x * gridSize + gridSize - 9;
      eye2Y = head.y * gridSize + gridSize - 9;
      break;
    case 'left':
      eye1X = head.x * gridSize + 5;
      eye1Y = head.y * gridSize + 5;
      eye2X = head.x * gridSize + 5;
      eye2Y = head.y * gridSize + gridSize - 9;
      break;
    case 'right':
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

// Desenhar a comida
function drawFood(food) {
  if (food.cheater) {
    // Comida trapaceira com cor oscilante
    const oscColor = oscillatingColor("#ff4444", "#ffff00", 0.01); // vermelho ↔ amarelo
    ctx.fillStyle = oscColor;
    ctx.shadowBlur = 25;
    ctx.shadowColor = oscColor;

    ctx.beginPath();
    ctx.arc(
      food.x * gridSize + gridSize/2,
      food.y * gridSize + gridSize/2,
      gridSize/2 - 2,
      0,
      Math.PI * 2
    );
    ctx.fill();
    ctx.shadowBlur = 0;
  } else if (food.special) {
    // comida especial
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--food-color');
    ctx.shadowBlur = 20;
    ctx.shadowColor = getComputedStyle(document.body).getPropertyValue('--food-color');
    ctx.beginPath();
    ctx.arc(
      food.x * gridSize + gridSize/2,
      food.y * gridSize + gridSize/2,
      gridSize/2,
      0, Math.PI * 2
    );
    ctx.fill();
    ctx.beginPath();
    ctx.arc(
      food.x * gridSize + gridSize/2,
      food.y * gridSize + gridSize/2,
      gridSize/2 + 3,
      0, Math.PI * 2
    );
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue('--food-color');
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.shadowBlur = 0;
  } else {
    // comida normal
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--food-color');
    ctx.shadowBlur = 15;
    ctx.shadowColor = getComputedStyle(document.body).getPropertyValue('--food-color');
    ctx.beginPath();
    ctx.arc(
      food.x * gridSize + gridSize/2,
      food.y * gridSize + gridSize/2,
      gridSize/2 - 2,
      0,
      Math.PI * 2
    );
    ctx.fill();
    ctx.shadowBlur = 0;
  }
}

// Animação de swap da comida trapaceira com easing
function animateFoodSwap(oldX, oldY, newX, newY) {
  let progress = 0;
  const steps = 15;

  const interval = setInterval(() => {
    progress++;
    const t = progress / steps;
    const easedT = easeInOutQuad(t); // função de easing no utils.js

    const interpX = oldX * gridSize + (newX - oldX) * gridSize * easedT;
    const interpY = oldY * gridSize + (newY - oldY) * gridSize * easedT;

    draw(gameState.snake, {
      ...gameState.food,
      x: interpX / gridSize,
      y: interpY / gridSize
    });

    if (progress >= steps) {
      clearInterval(interval);
    }
  }, 30);
}

function oscillatingColor(base1, base2, speed = 0.005) {
  const t = (Math.sin(Date.now() * speed) + 1) / 2; // varia entre 0 e 1
  const c1 = hexToRgb(base1);
  const c2 = hexToRgb(base2);
  const r = Math.round(c1.r + (c2.r - c1.r) * t);
  const g = Math.round(c1.g + (c2.g - c1.g) * t);
  const b = Math.round(c1.b + (c2.b - c1.b) * t);
  return `rgb(${r}, ${g}, ${b})`;
}

// Converter HEX para RGB
function hexToRgb(hex) {
  hex = hex.replace('#', '');
  if (hex.length === 3) {
    hex = hex.split('').map(c => c + c).join('');
  }
  const num = parseInt(hex, 16);
  return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
}

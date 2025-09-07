// Lógica principal do jogo

// Estado do jogo
const gameState = {
  snake: [],
  food: {},
  direction: 'right',
  nextDirection: 'right',
  score: 0,
  level: 1,
  highScore: localStorage.getItem('snakeHighScore') || 0,
  gameSpeed: 130,
  gameLoop: null,
  colorTheme: 1
};

// Elementos da UI
const uiElements = {
  score: document.getElementById('score'),
  highScore: document.getElementById('high-score'),
  level: document.getElementById('level'),
  speed: document.getElementById('speed'),
  finalScore: document.getElementById('final-score'),
  finalLevel: document.getElementById('final-level'),
  gameOver: document.getElementById('game-over'),
  restartBtn: document.getElementById('restart-btn')
};

// Configurações de redimensionamento dinâmico
const gridResizeConfig = {
  minWidth: 300,  // mínimo canvas width
  maxWidth: 600,  // máximo canvas width
  minHeight: 300, // mínimo canvas height
  maxHeight: 600, // máximo canvas height
  interval: 15000 // 15 segundos para mudar tamanho
};

// Inicializar o jogo
function initGame() {
  gameState.snake = [
    {x: 5, y: 10}, {x: 4, y: 10}, {x: 3, y: 10}
  ];
  generateFood();
  gameState.score = 0;
  gameState.level = 1;
  gameState.direction = 'right';
  gameState.nextDirection = 'right';
  gameState.gameSpeed = 130;

  updateScore();
  updateLevel();

  if (gameState.gameLoop) clearInterval(gameState.gameLoop);
  gameState.gameLoop = setInterval(gameUpdate, gameState.gameSpeed);

  uiElements.gameOver.style.display = 'none';
  document.body.className = 'color-theme-1';
  gameState.colorTheme = 1;
}

function startGridResizeLoop() {
  setInterval(() => {
    resizeGridDynamically();
  }, gridResizeConfig.interval);
}


// Gerar comida em posição aleatória
function generateFood() {
  const food = {
    x: Math.floor(Math.random() * (canvas.width / gridSize)),
    y: Math.floor(Math.random() * (canvas.height / gridSize)),
    special: Math.random() < 0.1,   // 10% especial
    cheater: Math.random() < 0.125 // 12.5% (1 em 8) trapaceira
  };

  // Verificar se a comida não está sobre a cobra
  if (isPositionOccupied(food.x, food.y, gameState.snake)) {
    return generateFood();
  }
  gameState.food = food;
}

// Atualizar a pontuação na UI
function updateScore() {
  uiElements.score.textContent = gameState.score;
  uiElements.highScore.textContent = gameState.highScore;
}

// Atualizar o nível na UI
function updateLevel() {
  uiElements.level.textContent = gameState.level;
  uiElements.speed.textContent = `${(1 + (gameState.level-1)*0.5).toFixed(1)}x`;
}

// Função para realmente comer a comida
function eatFood() {
  const points = gameState.food.special ? 5 : 1;
  gameState.score += points;

  if (gameState.score > gameState.highScore) {
    gameState.highScore = gameState.score;
    localStorage.setItem('snakeHighScore', gameState.highScore);
  }
  updateScore();

  // Subir de nível a cada 5 pontos
  const newLevel = Math.floor(gameState.score / 5) + 1;
  if (newLevel > gameState.level) {
    gameState.level = newLevel;
    updateLevel();

    gameState.gameSpeed = Math.max(50, 130 - (gameState.level-1)*15);
    clearInterval(gameState.gameLoop);
    gameState.gameLoop = setInterval(gameUpdate, gameState.gameSpeed);

    gameState.colorTheme = changeColorTheme();
    showAchievement(`Nível ${gameState.level} alcançado!`);
  }

  generateFood();
}

// Função para redimensionar grid/canvas dinamicamente
function resizeGridDynamically() {
  const newWidth = randomInt(gridResizeConfig.minWidth, gridResizeConfig.maxWidth);
  const newHeight = randomInt(gridResizeConfig.minHeight, gridResizeConfig.maxHeight);

  const oldCols = canvas.width / gridSize;
  const oldRows = canvas.height / gridSize;
  const newCols = Math.floor(newWidth / gridSize);
  const newRows = Math.floor(newHeight / gridSize);

  // Ajustar cobra para caber no novo tamanho
  gameState.snake = gameState.snake.map(seg => ({
    x: Math.min(seg.x, newCols - 1),
    y: Math.min(seg.y, newRows - 1)
  }));

  // Ajustar comida
  if (gameState.food.x >= newCols) gameState.food.x = newCols - 1;
  if (gameState.food.y >= newRows) gameState.food.y = newRows - 1;

  // Aplicar nova largura e altura no canvas
  canvas.width = newCols * gridSize;
  canvas.height = newRows * gridSize;

  // Animação suave via CSS
  canvas.style.transition = 'width 1s, height 1s';
  canvas.style.width = canvas.width + 'px';
  canvas.style.height = canvas.height + 'px';
}

// Iniciar loop de redimensionamento
function startGridResizeLoop() {
  setInterval(resizeGridDynamically, gridResizeConfig.interval);
}

// Atualizar o estado do jogo
function gameUpdate() {
  // Atualizar a direção
  gameState.direction = gameState.nextDirection;

  // Calcular a nova posição da cabeça
  const head = {...gameState.snake[0]};
  switch(gameState.direction) {
    case 'up': head.y--; break;
    case 'down': head.y++; break;
    case 'left': head.x--; break;
    case 'right': head.x++; break;
  }

  // Verificar colisões com as paredes
  if (head.x < 0 || head.x >= canvas.width / gridSize ||
      head.y < 0 || head.y >= canvas.height / gridSize) {
    shakeScreen();
    gameOver();
    return;
  }

  // Verificar colisão com o próprio corpo
  if (isPositionOccupied(head.x, head.y, gameState.snake)) {
    shakeScreen();
    gameOver();
    return;
  }

  // Adicionar nova cabeça
  gameState.snake.unshift(head);

  // Verificar se comeu a comida
  if (head.x === gameState.food.x && head.y === gameState.food.y) {

    if (gameState.food.cheater) {
      // Tenta fugir para uma casa adjacente
      const directions = [
        {x: 1, y: 0}, {x: -1, y: 0},
        {x: 0, y: 1}, {x: 0, y: -1}
      ];

      const validMoves = directions.filter(d => {
        const newX = gameState.food.x + d.x;
        const newY = gameState.food.y + d.y;
        return (
          newX >= 0 && newX < canvas.width / gridSize &&
          newY >= 0 && newY < canvas.height / gridSize &&
          !isPositionOccupied(newX, newY, gameState.snake)
        );
      });

      if (validMoves.length > 0) {
        const move = validMoves[Math.floor(Math.random() * validMoves.length)];
        const oldX = gameState.food.x;
        const oldY = gameState.food.y;

        gameState.food.x += move.x;
        gameState.food.y += move.y;
        gameState.food.cheater = false; // agora vira comida normal

        // Animação de swap
        animateFoodSwap(oldX, oldY, gameState.food.x, gameState.food.y);
      } else {
        // Sem escapatória -> cobra come
        eatFood();
      }

    } else {
      // Comida normal ou especial
      eatFood();
    }

  } else {
    // Remover a cauda se não comeu
    gameState.snake.pop();
  }

  // Desenhar o jogo
  draw(gameState.snake, gameState.food);
}

// Game over
function gameOver() {
  clearInterval(gameState.gameLoop);
  uiElements.finalScore.textContent = gameState.score;
  uiElements.finalLevel.textContent = gameState.level;
  uiElements.gameOver.style.display = 'flex';

  // enviar score para backend (se houver nome)
  try {
    const playerName = (window.souAthosScore && window.souAthosScore.getPlayerName) ? window.souAthosScore.getPlayerName() : "";
    if (playerName && typeof window.souAthosScore.postScoreIfHigh === "function") {
      window.souAthosScore.postScoreIfHigh(playerName, gameState.score);
    }
  } catch (e) {
    console.error("Erro ao postar score:", e);
  }
}

// Controles
document.addEventListener('keydown', function(e) {
  switch(e.key) {
    case 'ArrowUp': case 'w': case 'W':
      if (gameState.direction !== 'down') gameState.nextDirection = 'up';
      break;
    case 'ArrowDown': case 's': case 'S':
      if (gameState.direction !== 'up') gameState.nextDirection = 'down';
      break;
    case 'ArrowLeft': case 'a': case 'A':
      if (gameState.direction !== 'right') gameState.nextDirection = 'left';
      break;
    case 'ArrowRight': case 'd': case 'D':
      if (gameState.direction !== 'left') gameState.nextDirection = 'right';
      break;
  }
});

// Reiniciar o jogo
uiElements.restartBtn.addEventListener('click', initGame);

// Inicializar o jogo quando a página carregar
window.addEventListener('load', () => {
  createParticles();
  // iniciar loop de redimensionamento de grid
  startGridResizeLoop();
  updateScore();

  // não inicia automaticamente se não houver nome do jogador
  const playerName = (window.souAthosScore && window.souAthosScore.getPlayerName) ? window.souAthosScore.getPlayerName() : "";
  if (playerName && playerName.length > 0) {
    initGame();
  } else {
    // se não houver nome, o score modal (score.js) cuidará de iniciar o jogo ao clicar em jogar
    // garantir que o modal aparece e o campo esteja populado (feito em score.js)
  }
});

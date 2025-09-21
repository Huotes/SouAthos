// ==============================
// Estado global do jogo
// ==============================

export const gameState = {
  snake: [],
  food: {},
  direction: "right",
  nextDirection: "right",
  score: 0,
  level: 1,
  highScore: localStorage.getItem("snakeHighScore") || 0,
  gameSpeed: 130,
  gameLoop: null,
  colorTheme: 1,
};

// ==============================
// Configurações de redimensionamento
// ==============================
export const gridResizeConfig = {
  minWidth: 300,
  maxWidth: 600,
  minHeight: 300,
  maxHeight: 600,
  interval: 15000,
};


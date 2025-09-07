// Utilitários e funções auxiliares

// Criar partículas de fundo animadas
function createParticles() {
  const bgContainer = document.getElementById('animated-bg');
  const particleCount = 50;
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    const size = Math.random() * 10 + 2;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.animation = `float ${Math.random() * 10 + 10}s linear infinite`;
    particle.style.animationDelay = `${Math.random() * 5}s`;
    
    // Cor aleatória para as partículas
    const colors = ['#0ff', '#f0f', '#ff0', '#0f0', '#f00'];
    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
    
    bgContainer.appendChild(particle);
  }
}

// Mostrar conquista
function showAchievement(text) {
  const achievement = document.getElementById('achievement');
  const achievementText = document.getElementById('achievement-text');
  
  achievementText.textContent = text;
  achievement.classList.add('show');
  
  setTimeout(() => {
    achievement.classList.remove('show');
  }, 3000);
}

// Efeito de tremer a tela
function shakeScreen() {
  const gameContainer = document.getElementById('game-container');
  gameContainer.classList.add('shake');
  
  setTimeout(() => {
    gameContainer.classList.remove('shake');
  }, 500);
}

// Mudar tema de cores
function changeColorTheme() {
  const body = document.body;
  const currentTheme = parseInt(body.className.replace('color-theme-', ''));
  const newTheme = (currentTheme % 5) + 1;
  
  body.className = `color-theme-${newTheme}`;
  return newTheme;
}

// Gerar número aleatório dentro de um intervalo
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Verificar se um objeto está em uma posição específica
function isPositionOccupied(x, y, array) {
  return array.some(item => item.x === x && item.y === y);
}

// Função de easing (ease-in-out)
function easeInOutQuad(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}


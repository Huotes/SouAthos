// js/utils/utils.js
// Utilitários e funções auxiliares

export const particles = []; // partículas para explosões no canvas (opcional)

// ===============================
// Partículas de fundo animadas (fora do canvas)
// ===============================
export function createParticles() {
  const container = document.getElementById("animated-bg");
  if (!container) return;

  function spawnParticles() {
    container.innerHTML = ""; // limpa partículas antigas

    const numParticles = Math.floor((window.innerWidth * window.innerHeight) / 12000);

    for (let i = 0; i < numParticles; i++) {
      const particle = document.createElement("div");
      particle.classList.add("particle");

      const size = Math.random() * 6 + 2; // 2px a 8px
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;

      particle.style.left = `${Math.random() * 100}%`;
      particle.style.top = `${Math.random() * 100}%`;

      particle.style.animation = `float ${5 + Math.random() * 10}s linear infinite`;
      particle.style.opacity = (Math.random() * 0.5 + 0.2).toFixed(2);

      // cores coloridas aleatórias
      const colors = ["#0ff", "#ff0", "#f0f", "#ff6b6b", "#4ecdc4"];
      particle.style.background = colors[Math.floor(Math.random() * colors.length)];

      container.appendChild(particle);
    }
  }

  spawnParticles();
  window.addEventListener("resize", spawnParticles);
}

// ===============================
// Explosão de partículas no canvas (opcional para efeitos de nível)
// ===============================
export function createExplosion(origin, count = 30, color = "#0ff") {
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * 2 * Math.PI;
    const speed = Math.random() * 2 + 0.5;
    particles.push({
      x: origin.x,
      y: origin.y,
      dx: Math.cos(angle) * speed,
      dy: Math.sin(angle) * speed,
      r: Math.random() * 3 + 1,
      life: 50 + Math.random() * 30,
      color: color
    });
  }
}

// ===============================
// Atualiza partículas no canvas (se houver)
// ===============================
export function updateParticles(ctx) {
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.dx;
    p.y += p.dy;
    p.life--;

    ctx.fillStyle = p.color;
    ctx.globalAlpha = Math.max(p.life / 80, 0);
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();

    if (p.life <= 0) particles.splice(i, 1);
  }
  ctx.globalAlpha = 1;
}

// ===============================
// Mostrar conquista
// ===============================
export function showAchievement(text) {
  const achievement = document.getElementById('achievement');
  const achievementText = document.getElementById('achievement-text');
  
  achievementText.textContent = text;
  achievement.classList.add('show');
  
  setTimeout(() => achievement.classList.remove('show'), 3000);
}

// ===============================
// Efeito de tremer a tela
// ===============================
export function shakeScreen() {
  const gameContainer = document.getElementById('game-container');
  gameContainer.classList.add('shake');
  
  setTimeout(() => gameContainer.classList.remove('shake'), 500);
}

// ===============================
// Mudar tema de cores
// ===============================
export function changeColorTheme() {
  const body = document.body;
  const currentTheme = parseInt(body.className.replace('color-theme-', '')) || 1;
  const newTheme = (currentTheme % 5) + 1;
  body.className = `color-theme-${newTheme}`;
  return newTheme;
}

// ===============================
// Gerar número aleatório
// ===============================
export function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// ===============================
// Verificar se posição está ocupada
// ===============================
export function isPositionOccupied(x, y, array) {
  return array.some(item => item.x === x && item.y === y);
}

// ===============================
// Função de easing (ease-in-out)
export function easeInOutQuad(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

// ===============================
// Mistura de cores HEX
// ===============================
function mixHex(a, b, t) {
  const ah = a.replace('#',''); 
  const bh = b.replace('#','');
  const ai = [0,2,4].map(i => parseInt(ah.slice(i,i+2),16));
  const bi = [0,2,4].map(i => parseInt(bh.slice(i,i+2),16));
  const ci = ai.map((av, i) => Math.round(av + (bi[i]-av)*t));
  return '#' + ci.map(v => v.toString(16).padStart(2,'0')).join('');
}

// ===============================
// Pisca suavemente entre duas cores
// ===============================
export function oscillatingColor(colorA, colorB, speed = 0.012) {
  const t = (1 + Math.sin(Date.now() * speed)) / 2;
  return mixHex(colorA, colorB, t);
}


"""
Configurações centralizadas do Snake Game
Princípio DRY: Todas as constantes em um local
"""

from typing import Tuple

# =============================================================================
# CONFIGURAÇÕES DA JANELA
# =============================================================================
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
WINDOW_TITLE: str = "Snake Game - Python 3.13"

# =============================================================================
# CONFIGURAÇÕES DO GRID
# =============================================================================
GRID_SIZE: int = 20
GRID_WIDTH: int = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT: int = WINDOW_HEIGHT // GRID_SIZE

# =============================================================================
# CONFIGURAÇÕES DE GAMEPLAY
# =============================================================================
BASE_FPS: int = 8  # FPS inicial (mais lento)
MAX_FPS: int = 20  # FPS máximo
FPS_INCREASE_PER_LEVEL: float = 1.2  # Multiplicador de velocidade por nível
INITIAL_SNAKE_LENGTH: int = 1
POINTS_PER_FOOD: int = 1  # 1 ponto por fruta normal
POINTS_PER_LEVEL: int = 10  # A cada 10 pontos sobe de nível

# Configurações das comidas especiais
SPECIAL_FOOD_POINTS: int = 5  # 5 pontos para comida especial
SPECIAL_FOOD_SPAWN_CHANCE: float = 0.15  # 15% de chance de spawnar especial
FUGITIVE_FOOD_SPAWN_CHANCE: float = 0.10  # 10% de chance de spawnar fugitiva
FUGITIVE_FOOD_TRAIL_DURATION: float = 1.5  # Duração do rastro em segundos
FUGITIVE_FOOD_BLINK_SPEED: float = 3.0  # Velocidade do piscar
FUGITIVE_FOOD_POINTS: int = 3  # 3 pontos para comida fugitiva

# =============================================================================
# CORES (RGB)
# =============================================================================
class Colors:
    """Classe para centralizar todas as cores do jogo"""
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    DARK_GREEN: Tuple[int, int, int] = (0, 128, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    GRAY: Tuple[int, int, int] = (128, 128, 128)
    LIGHT_GRAY: Tuple[int, int, int] = (200, 200, 200)
    
    # Grid transparente
    GRID_ALPHA: Tuple[int, int, int, int] = (128, 128, 128, 50)  # Cinza com alpha
    
    # Cores do efeito level up (arco-íris)
    RAINBOW_COLORS = [
        (255, 0, 0),    # Vermelho
        (255, 127, 0),  # Laranja  
        (255, 255, 0),  # Amarelo
        (0, 255, 0),    # Verde
        (0, 0, 255),    # Azul
        (75, 0, 130),   # Índigo
        (148, 0, 211),  # Violeta
    ]
    
    # Cores das comidas especiais
    SPECIAL_FOOD_COLOR: Tuple[int, int, int] = (255, 215, 0)  # Dourado
    SPECIAL_FOOD_BORDER: Tuple[int, int, int] = (255, 165, 0)  # Laranja dourado
    FUGITIVE_FOOD_COLOR: Tuple[int, int, int] = (138, 43, 226)  # Violeta
    FUGITIVE_FOOD_TRAIL: Tuple[int, int, int, int] = (138, 43, 226, 100)  # Violeta transparente

# =============================================================================
# CONFIGURAÇÕES DE FONTES
# =============================================================================
class FontSizes:
    """Tamanhos de fontes para diferentes elementos da UI"""
    SMALL: int = 24
    MEDIUM: int = 36
    LARGE: int = 48
    EXTRA_LARGE: int = 72

# =============================================================================
# CONFIGURAÇÕES DE CONTROLES
# =============================================================================
class Controls:
    """Mapeamento de controles do jogo"""
    # Movimento
    MOVE_UP = ['K_UP', 'K_w']
    MOVE_DOWN = ['K_DOWN', 'K_s'] 
    MOVE_LEFT = ['K_LEFT', 'K_a']
    MOVE_RIGHT = ['K_RIGHT', 'K_d']
    
    # Ações do jogo
    RESTART = 'K_r'
    QUIT = 'K_q'
    PAUSE = 'K_SPACE'

# =============================================================================
# CONFIGURAÇÕES DE EFEITOS VISUAIS  
# =============================================================================
class Effects:
    """Configurações para efeitos visuais"""
    LEVEL_UP_FLASH_DURATION: float = 2.0  # Duração do flash em segundos
    LEVEL_UP_FLASH_SPEED: float = 0.1     # Velocidade da animação
    GRID_TRANSPARENCY: int = 30            # Transparência do grid (0-255)
# =============================================================================
# CONFIGURAÇÕES DE POSIÇÕES INICIAIS
# =============================================================================
INITIAL_SNAKE_X: int = GRID_WIDTH // 2
INITIAL_SNAKE_Y: int = GRID_HEIGHT // 2

# =============================================================================
# MENSAGENS DO JOGO
# =============================================================================
class Messages:
    """Mensagens exibidas no jogo"""
    GAME_OVER: str = "GAME OVER"
    RESTART_INSTRUCTION: str = "Pressione R para reiniciar ou Q para sair"
    FINAL_SCORE: str = "Score Final: {score}"
    CURRENT_SCORE: str = "Score: {score}"
    SNAKE_LENGTH: str = "Length: {length}"
    CURRENT_LEVEL: str = "Level: {level}"
    SPEED_INFO: str = "Speed: {speed:.1f}x"
    LEVEL_UP: str = "LEVEL UP!"
    PAUSED: str = "PAUSADO - Pressione SPACE para continuar"

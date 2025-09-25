"""
Configurações centralizadas do Snake Game com tema Gruvbox
Princípio DRY: Todas as constantes em um local
Tema Gruvbox Dark implementado com paleta completa
"""

from typing import Tuple

# =============================================================================
# CONFIGURAÇÕES DA JANELA
# =============================================================================
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
WINDOW_TITLE: str = "Snake Game - Python 3.13 | Tema Gruvbox"

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
SPECIAL_FOOD_SPAWN_CHANCE: float = 0.12  # 12% de chance de spawnar especial
FUGITIVE_FOOD_SPAWN_CHANCE: float = 0.08  # 8% de chance de spawnar fugitiva
MIRROR_FOOD_SPAWN_CHANCE: float = 0.05  # 5% de chance de spawnar espelho
FUGITIVE_FOOD_TRAIL_DURATION: float = 1.5  # Duração do rastro em segundos
FUGITIVE_FOOD_BLINK_SPEED: float = 3.0  # Velocidade do piscar
FUGITIVE_FOOD_POINTS: int = 3  # 3 pontos para comida fugitiva
MIRROR_FOOD_POINTS: int = 2  # 2 pontos para comida espelho

# =============================================================================
# PALETA DE CORES GRUVBOX (DARK MODE)
# =============================================================================
class Colors:
    """Paleta completa de cores Gruvbox Dark Mode"""
    
    # Cores de background (fundo)
    BG_DARK: Tuple[int, int, int] = (40, 40, 40)        # bg0_h
    BG_MEDIUM: Tuple[int, int, int] = (29, 32, 33)      # bg0
    BG_LIGHT: Tuple[int, int, int] = (50, 48, 47)       # bg1
    BG_LIGHTER: Tuple[int, int, int] = (60, 56, 54)     # bg2
    BG_LIGHTEST: Tuple[int, int, int] = (80, 73, 69)    # bg3
    
    # Cores de foreground (texto)
    FG_DARK: Tuple[int, int, int] = (157, 0, 6)         # fg0
    FG_MEDIUM: Tuple[int, int, int] = (235, 219, 178)   # fg1
    FG_LIGHT: Tuple[int, int, int] = (251, 241, 199)    # fg2
    
    # Cores neutras
    GRAY_DARK: Tuple[int, int, int] = (124, 111, 100)   # gray0
    GRAY_LIGHT: Tuple[int, int, int] = (146, 131, 116)  # gray1
    
    # Cores vermelhas
    RED_DARK: Tuple[int, int, int] = (204, 36, 29)      # red0
    RED_LIGHT: Tuple[int, int, int] = (251, 73, 52)     # red1
    RED_BRIGHT: Tuple[int, int, int] = (255, 85, 85)    # red2
    
    # Cores verdes
    GREEN_DARK: Tuple[int, int, int] = (152, 151, 26)   # green0
    GREEN_LIGHT: Tuple[int, int, int] = (184, 187, 38)  # green1
    GREEN_BRIGHT: Tuple[int, int, int] = (168, 153, 132) # green2
    
    # Cores amarelas/laranjas
    YELLOW_DARK: Tuple[int, int, int] = (215, 153, 33)  # yellow0
    YELLOW_LIGHT: Tuple[int, int, int] = (250, 189, 47) # yellow1
    YELLOW_BRIGHT: Tuple[int, int, int] = (255, 213, 0) # yellow2
    
    ORANGE_DARK: Tuple[int, int, int] = (214, 93, 14)   # orange0
    ORANGE_LIGHT: Tuple[int, int, int] = (254, 128, 25) # orange1
    ORANGE_BRIGHT: Tuple[int, int, int] = (255, 165, 0) # orange2
    
    # Cores azuis
    BLUE_DARK: Tuple[int, int, int] = (69, 133, 136)    # blue0
    BLUE_LIGHT: Tuple[int, int, int] = (131, 165, 152)  # blue1
    BLUE_BRIGHT: Tuple[int, int, int] = (109, 188, 247) # blue2
    
    # Cores roxas
    PURPLE_DARK: Tuple[int, int, int] = (177, 98, 134)  # purple0
    PURPLE_LIGHT: Tuple[int, int, int] = (211, 134, 155) # purple1
    PURPLE_BRIGHT: Tuple[int, int, int] = (212, 80, 135) # purple2
    
    # Cores aqua/cyan
    AQUA_DARK: Tuple[int, int, int] = (104, 157, 106)   # aqua0
    AQUA_LIGHT: Tuple[int, int, int] = (142, 192, 124)  # aqua1
    AQUA_BRIGHT: Tuple[int, int, int] = (137, 220, 235) # aqua2
    
    # Cores para elementos específicos
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    
    # Cores da cobra
    SNAKE_HEAD: Tuple[int, int, int] = GREEN_LIGHT      # Cabeça da cobra
    SNAKE_BODY: Tuple[int, int, int] = GREEN_DARK       # Corpo da cobra
    SNAKE_TAIL: Tuple[int, int, int] = AQUA_LIGHT       # Cauda da cobra
    
    # Cores das comidas
    FOOD_NORMAL: Tuple[int, int, int] = RED_LIGHT       # Comida normal
    FOOD_SPECIAL: Tuple[int, int, int] = YELLOW_LIGHT   # Comida especial
    FOOD_FUGITIVE: Tuple[int, int, int] = PURPLE_LIGHT  # Comida fugitiva
    FOOD_MIRROR: Tuple[int, int, int] = BLUE_LIGHT      # Comida espelho
    
    # Bordas das comidas
    FOOD_BORDER_NORMAL: Tuple[int, int, int] = RED_DARK
    FOOD_BORDER_SPECIAL: Tuple[int, int, int] = ORANGE_LIGHT
    FOOD_BORDER_FUGITIVE: Tuple[int, int, int] = PURPLE_BRIGHT
    FOOD_BORDER_MIRROR: Tuple[int, int, int] = AQUA_BRIGHT
    
    # Cores de efeitos visuais
    SHADOW_COLOR: Tuple[int, int, int] = BLACK
    GRID_COLOR: Tuple[int, int, int] = GRAY_DARK
    HIGHLIGHT_COLOR: Tuple[int, int, int] = YELLOW_BRIGHT
    
    # Cores da UI
    UI_BACKGROUND: Tuple[int, int, int] = BG_LIGHT
    UI_FOREGROUND: Tuple[int, int, int] = FG_MEDIUM
    UI_BORDER: Tuple[int, int, int] = GRAY_LIGHT
    UI_HIGHLIGHT: Tuple[int, int, int] = ORANGE_LIGHT
    UI_WARNING: Tuple[int, int, int] = RED_LIGHT
    UI_SUCCESS: Tuple[int, int, int] = GREEN_LIGHT
    UI_INFO: Tuple[int, int, int] = BLUE_LIGHT
    
    # Cores para texto
    TEXT_PRIMARY: Tuple[int, int, int] = FG_MEDIUM
    TEXT_SECONDARY: Tuple[int, int, int] = GRAY_LIGHT
    TEXT_ACCENT: Tuple[int, int, int] = ORANGE_LIGHT
    TEXT_WARNING: Tuple[int, int, int] = YELLOW_LIGHT
    TEXT_ERROR: Tuple[int, int, int] = RED_LIGHT
    TEXT_SUCCESS: Tuple[int, int, int] = GREEN_LIGHT
    
    # Cores para efeitos de partículas
    PARTICLE_PRIMARY: Tuple[int, int, int] = ORANGE_LIGHT
    PARTICLE_SECONDARY: Tuple[int, int, int] = YELLOW_LIGHT
    PARTICLE_ACCENT: Tuple[int, int, int] = RED_LIGHT
    
    # Cores do arco-íris para efeitos especiais
    RAINBOW_COLORS = [
        RED_LIGHT,      # Vermelho
        ORANGE_LIGHT,   # Laranja
        YELLOW_LIGHT,   # Amarelo
        GREEN_LIGHT,    # Verde
        AQUA_LIGHT,     # Aqua
        BLUE_LIGHT,     # Azul
        PURPLE_LIGHT,   # Roxo
    ]
    
    # Gradientes Gruvbox
    GRADIENT_BG = [BG_DARK, BG_MEDIUM, BG_LIGHT]
    GRADIENT_WARM = [RED_LIGHT, ORANGE_LIGHT, YELLOW_LIGHT]
    GRADIENT_COOL = [GREEN_LIGHT, AQUA_LIGHT, BLUE_LIGHT]

# =============================================================================
# CONFIGURAÇÕES DE FONTES
# =============================================================================
class FontSizes:
    """Tamanhos de fontes para diferentes elementos da UI"""
    TINY: int = 14
    SMALL: int = 18
    MEDIUM: int = 24
    LARGE: int = 32
    EXTRA_LARGE: int = 48
    MASSIVE: int = 64

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
    TOGGLE_FULLSCREEN = 'K_f'
    TOGGLE_DEBUG = 'K_F3'
    
    # Navegação de menu
    MENU_UP = ['K_UP', 'K_w']
    MENU_DOWN = ['K_DOWN', 'K_s']
    MENU_SELECT = ['K_RETURN', 'K_SPACE']
    MENU_BACK = 'K_ESCAPE'

# =============================================================================
# CONFIGURAÇÕES DE EFEITOS VISUAIS
# =============================================================================
class Effects:
    """Configurações para efeitos visuais avançados"""
    
    # Durações de efeitos (em segundos)
    LEVEL_UP_FLASH_DURATION: float = 2.0
    MIRROR_EFFECT_DURATION: float = 0.5
    SPECIAL_CONSUME_EFFECT_DURATION: float = 1.0
    SCREEN_SHAKE_DURATION: float = 0.3
    PARTICLE_LIFETIME: float = 2.0
    
    # Intensidades
    GRID_TRANSPARENCY: int = 30
    SCREEN_FLASH_INTENSITY: int = 100
    SHADOW_ALPHA: int = 140
    SCREEN_SHAKE_INTENSITY: float = 5.0
    
    # Contagens
    PARTICLE_BURST_COUNT: int = 12
    AMBIENT_PARTICLE_COUNT: int = 25
    MAX_PARTICLES: int = 100
    
    # Velocidades de animação
    LEVEL_UP_FLASH_SPEED: float = 0.1
    PARTICLE_SPEED_MULTIPLIER: float = 1.0
    AMBIENT_PARTICLE_SPEED: float = 15.0
    
    # Layout e UI
    UI_CORNER_RADIUS: int = 12
    UI_PADDING: int = 16
    UI_SHADOW_INTENSITY: int = 120
    UI_BORDER_WIDTH: int = 2
    
    # Sombras
    SHADOW_OFFSET: int = 6
    SHADOW_BLUR_RADIUS: int = 8
    GLOW_INTENSITY: int = 80
    
    # Efeitos específicos
    FUGITIVE_FOOD_BLINK_SPEED: float = 3.0
    FUGITIVE_FOOD_TRAIL_DURATION: float = 1.5
    SNAKE_MOVEMENT_SMOOTHING: float = 0.8

# =============================================================================
# CONFIGURAÇÕES DE ÁUDIO
# =============================================================================
class Audio:
    """Configurações de áudio e sons"""
    
    # Volumes (0.0 - 1.0)
    MASTER_VOLUME: float = 1.0
    MUSIC_VOLUME: float = 0.7
    SFX_VOLUME: float = 0.8
    
    # Pitch variations
    PITCH_VARIATION: float = 0.1
    
    # Sound file paths (para referência futura)
    SOUND_EAT: str = "sounds/eat.wav"
    SOUND_LEVEL_UP: str = "sounds/level_up.wav"
    SOUND_GAME_OVER: str = "sounds/game_over.wav"
    SOUND_SPECIAL: str = "sounds/special.wav"

# =============================================================================
# CONFIGURAÇÕES DE POSIÇÕES INICIAIS
# =============================================================================
INITIAL_SNAKE_X: int = GRID_WIDTH // 2
INITIAL_SNAKE_Y: int = GRID_HEIGHT // 2
INITIAL_DIRECTION: str = 'RIGHT'

# =============================================================================
# CONFIGURAÇÕES DE DIFICULDADE
# =============================================================================
class Difficulty:
    """Configurações de dificuldade do jogo"""
    
    EASY = {
        'base_fps': 6,
        'max_fps': 15,
        'fps_increase': 1.1,
        'special_food_chance': 0.15,
        'points_per_level': 8
    }
    
    NORMAL = {
        'base_fps': 8,
        'max_fps': 20,
        'fps_increase': 1.2,
        'special_food_chance': 0.12,
        'points_per_level': 10
    }
    
    HARD = {
        'base_fps': 10,
        'max_fps': 25,
        'fps_increase': 1.3,
        'special_food_chance': 0.08,
        'points_per_level': 12
    }
    
    EXPERT = {
        'base_fps': 12,
        'max_fps': 30,
        'fps_increase': 1.4,
        'special_food_chance': 0.05,
        'points_per_level': 15
    }

# =============================================================================
# MENSAGENS DO JOGO
# =============================================================================
class Messages:
    """Mensagens exibidas no jogo"""
    
    GAME_OVER: str = "FIM DE JOGO"
    RESTART_INSTRUCTION: str = "Pressione R para reiniciar ou Q para sair"
    FINAL_SCORE: str = "Pontuação Final: {score}"
    CURRENT_SCORE: str = "Pontos: {score}"
    SNAKE_LENGTH: str = "Tamanho: {length}"
    CURRENT_LEVEL: str = "Nível: {level}"
    SPEED_INFO: str = "Velocidade: {speed:.1f}x"
    LEVEL_UP: str = "NIVEL AUMENTADO!"
    PAUSED: str = "PAUSADO - Pressione ESPAÇO para continuar"
    
    # Novas mensagens
    DIFFICULTY_SELECT: str = "Selecione a Dificuldade"
    HIGH_SCORE: str = "Recorde: {score}"
    NEW_HIGH_SCORE: str = "NOVO RECORDE!"
    SPECIAL_FOOD_EATEN: str = "Comida Especial!"
    FUGITIVE_FOOD_EATEN: str = "Comida Fugitiva!"
    MIRROR_FOOD_EATEN: str = "Comida Espelho!"
    
    # Instruções
    CONTROLS_HELP: str = "Controles: WASD/Setas - Mover | ESPAÇO - Pausar | R - Reiniciar"
    OBJECTIVE: str = "Objetivo: Coma as frutas para crescer e evitar colisões!"

# =============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# =============================================================================
class Performance:
    """Configurações de otimização e performance"""
    
    MAX_FRAME_SKIP: int = 5
    TARGET_FPS: int = 60
    VSYNC: bool = True
    DOUBLE_BUFFER: bool = True
    HARDWARE_ACCELERATION: bool = True
    
    # Otimizações de partículas
    PARTICLE_UPDATE_RATE: int = 30  # FPS máximo para atualização de partículas
    AMBIENT_PARTICLES_ENABLED: bool = True
    PARTICLE_EFFECTS_ENABLED: bool = True
    
    # Cache
    SURFACE_CACHE_ENABLED: bool = True
    MAX_CACHED_SURFACES: int = 50

# =============================================================================
# CONFIGURAÇÕES DE DEBUG
# =============================================================================
class Debug:
    """Configurações para modo de depuração"""
    
    SHOW_FPS: bool = False
    SHOW_COLLISION_BOXES: bool = False
    SHOW_GRID_COORDINATES: bool = False
    SHOW_PARTICLE_COUNT: bool = False
    SHOW_PERFORMANCE_STATS: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_TO_FILE: bool = False
    LOG_FILE: str = "snake_game.log"

# =============================================================================
# CONSTANTES GLOBAIS
# =============================================================================
VERSION: str = "3.0.0"
AUTHOR: str = "Snake Game Python"
GAME_NAME: str = "Python Snake Game - Gruvbox Edition"

# Direções possíveis para a cobra
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# Estados do jogo
class GameStates:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_UP = "level_up"

print("✅ Configurações Gruvbox carregadas com sucesso!")

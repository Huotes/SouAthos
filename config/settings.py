"""
Configurações centralizadas do Snake Game v3.0
Princípio DRY: Todas as constantes em um local
Tema Gruvbox + Gráficos avançados + Compatibilidade total
"""

from typing import Tuple, List

# =============================================================================
# CONFIGURAÇÕES DA JANELA
# =============================================================================
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
WINDOW_TITLE: str = "Snake Game v3.0 - Gruvbox Edition"

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

# Configurações das comidas especiais (balanceadas para v3.0)
SPECIAL_FOOD_POINTS: int = 5  # 5 pontos para comida especial
SPECIAL_FOOD_SPAWN_CHANCE: float = 0.12  # 12% de chance de spawnar especial
FUGITIVE_FOOD_SPAWN_CHANCE: float = 0.08  # 8% de chance de spawnar fugitiva
MIRROR_FOOD_SPAWN_CHANCE: float = 0.05  # 5% de chance de spawnar espelho
FUGITIVE_FOOD_TRAIL_DURATION: float = 1.5  # Duração do rastro em segundos
FUGITIVE_FOOD_BLINK_SPEED: float = 3.0  # Velocidade do piscar
FUGITIVE_FOOD_POINTS: int = 3  # 3 pontos para comida fugitiva
MIRROR_FOOD_POINTS: int = 2  # 2 pontos para comida espelho

# =============================================================================
# PALETA DE CORES GRUVBOX v3.0 (RGB)
# =============================================================================
class Colors:
    """
    Paleta de cores Gruvbox completa para o Snake Game v3.0
    
    Baseada na paleta oficial do tema Gruvbox para terminais
    Cores organizadas por categoria para fácil manutenção
    """
    
    # === CORES BASE GRUVBOX ===
    BG_DARK = (40, 40, 40)          # #282828 - Fundo escuro principal
    BG_MEDIUM = (60, 56, 54)        # #3c3836 - Fundo médio
    BG_LIGHT = (80, 73, 69)         # #504945 - Fundo claro
    BG_LIGHTER = (102, 92, 84)      # #665c54 - Fundo mais claro
    
    FG_LIGHT = (235, 219, 178)      # #ebdbb2 - Texto claro principal
    FG_MEDIUM = (213, 196, 161)     # #d5c4a1 - Texto médio
    FG_DARK = (146, 131, 116)       # #928374 - Texto escuro
    
    # === CORES DE DESTAQUE GRUVBOX ===
    RED = (204, 36, 29)             # #cc241d - Vermelho Gruvbox
    GREEN = (152, 151, 26)          # #98971a - Verde Gruvbox
    YELLOW = (215, 153, 33)         # #d79921 - Amarelo Gruvbox
    BLUE = (69, 133, 136)           # #458588 - Azul Gruvbox
    PURPLE = (177, 98, 134)         # #b16286 - Roxo Gruvbox
    AQUA = (104, 157, 106)          # #689d6a - Aqua Gruvbox
    ORANGE = (214, 93, 14)          # #d65d0e - Laranja Gruvbox
    
    # === CORES BRILHANTES GRUVBOX ===
    BRIGHT_RED = (251, 73, 52)      # #fb4934 - Vermelho brilhante
    BRIGHT_GREEN = (184, 187, 38)   # #b8bb26 - Verde brilhante
    BRIGHT_YELLOW = (250, 189, 47)  # #fabd2f - Amarelo brilhante
    BRIGHT_BLUE = (131, 165, 152)   # #83a598 - Azul brilhante
    BRIGHT_PURPLE = (211, 134, 155) # #d3869b - Roxo brilhante
    BRIGHT_AQUA = (142, 192, 124)   # #8ec07c - Aqua brilhante
    BRIGHT_ORANGE = (254, 128, 25)  # #fe8019 - Laranja brilhante
    
    # === MAPEAMENTO PARA ELEMENTOS ESPECÍFICOS ===
    
    # Grid e Background
    BACKGROUND = BG_DARK             # Fundo principal
    GRID_COLOR = BG_MEDIUM           # Cor do grid
    SHADOW_COLOR = (29, 32, 33)      # #1d2021 - Cor das sombras
    
    # Snake (Cobra)
    SNAKE_HEAD = BRIGHT_GREEN        # Verde brilhante para cabeça
    SNAKE_BODY = GREEN               # Verde normal para corpo
    SNAKE_EYE = FG_LIGHT            # Branco para olhos
    SNAKE_PUPIL = BG_DARK           # Escuro para pupila
    
    # Foods (Comidas) - Cores específicas por tipo
    FOOD_NORMAL = BRIGHT_RED         # Vermelho brilhante (comida normal)
    FOOD_SPECIAL = BRIGHT_YELLOW     # Amarelo dourado (comida especial)
    FOOD_FUGITIVE = BRIGHT_PURPLE    # Roxo brilhante (comida fugitiva)
    FOOD_MIRROR = BRIGHT_BLUE        # Azul brilhante (comida espelho)
    
    # UI e Interface
    UI_PRIMARY = FG_LIGHT            # Texto principal da UI
    UI_SECONDARY = FG_MEDIUM         # Texto secundário da UI
    UI_ACCENT = BRIGHT_YELLOW        # Cor de destaque da UI
    UI_BACKGROUND = BG_MEDIUM        # Fundo dos painéis da UI
    UI_BORDER = FG_DARK             # Bordas dos elementos da UI
    
    # Efeitos e Partículas
    PARTICLE_GLOW = BRIGHT_YELLOW    # Brilho das partículas
    LEVEL_UP_GLOW = BRIGHT_GREEN     # Brilho do level up
    FLASH_DEFAULT = BRIGHT_YELLOW    # Flash padrão da tela
    
    # Grid Level Up - Cores do arco-íris Gruvbox
    RAINBOW_COLORS: List[Tuple[int, int, int]] = [
        BRIGHT_RED,      # Vermelho brilhante
        BRIGHT_ORANGE,   # Laranja brilhante
        BRIGHT_YELLOW,   # Amarelo brilhante
        BRIGHT_GREEN,    # Verde brilhante
        BRIGHT_BLUE,     # Azul brilhante
        PURPLE,          # Roxo normal
        BRIGHT_PURPLE,   # Roxo brilhante
    ]
    
    # === ALIASES PARA COMPATIBILIDADE ===
    BLACK = BG_DARK                  # Compatibilidade
    WHITE = FG_LIGHT                 # Compatibilidade  
    GRAY = FG_DARK                   # Compatibilidade
    LIGHT_GRAY = FG_MEDIUM           # Compatibilidade
    
    # Aliases específicos para elementos antigos
    DARK_GREEN = GREEN               # Compatibilidade com código antigo
    SPECIAL_FOOD_COLOR = FOOD_SPECIAL
    SPECIAL_FOOD_BORDER = ORANGE
    FUGITIVE_FOOD_COLOR = FOOD_FUGITIVE
    MIRROR_FOOD_COLOR = FOOD_MIRROR
    MIRROR_FOOD_BORDER = BLUE

# =============================================================================
# CONFIGURAÇÕES DE EFEITOS VISUAIS v3.0
# =============================================================================
class Effects:
    """
    Configurações para todos os efeitos visuais v3.0
    
    Otimizado para performance e experiência visual moderna
    Compatível com renderer avançado e sistema de partículas
    """
    
    # === EFEITOS BÁSICOS ===
    LEVEL_UP_FLASH_DURATION: float = 2.5     # Duração do flash de level up (segundos)
    LEVEL_UP_FLASH_SPEED: float = 0.08       # Velocidade da animação (mais suave)
    GRID_TRANSPARENCY: int = 45               # Transparência do grid (0-255)
    
    # === EFEITOS DE CONSUMO DE COMIDAS ===
    SPECIAL_CONSUME_EFFECT_DURATION: float = 1.2   # Duração dos efeitos especiais
    MIRROR_EFFECT_DURATION: float = 0.8            # Duração da inversão do espelho
    SCREEN_FLASH_INTENSITY: int = 120              # Intensidade do flash na tela (0-255)
    PARTICLE_BURST_COUNT: int = 12                 # Partículas no burst de consumo
    
    # === ANIMAÇÕES FLUIDAS ===
    SNAKE_SCALE_ANIMATION: float = 0.1             # Amplitude da animação da cobra
    FOOD_PULSE_SPEED: float = 2.0                  # Velocidade do pulse das comidas
    FOOD_GLOW_INTENSITY: float = 0.4               # Intensidade do brilho das comidas
    UI_ANIMATION_SPEED: float = 3.0                # Velocidade das animações da UI
    
    # === SOMBRAS E PROFUNDIDADE ===
    SHADOW_OFFSET: int = 2                         # Deslocamento das sombras (pixels)
    SHADOW_BLUR: int = 3                           # Desfoque das sombras (camadas)
    SHADOW_ALPHA: int = 100                        # Transparência das sombras (0-255)
    
    # === SISTEMA DE PARTÍCULAS AMBIENTAIS ===
    AMBIENT_PARTICLE_COUNT: int = 15               # Número de partículas flutuando
    AMBIENT_PARTICLE_SPEED: float = 15.0           # Velocidade base das partículas
    AMBIENT_PARTICLE_ALPHA_MIN: int = 20           # Alpha mínimo das partículas
    AMBIENT_PARTICLE_ALPHA_MAX: int = 60           # Alpha máximo das partículas
    AMBIENT_PARTICLE_SIZE_MIN: float = 0.5         # Tamanho mínimo das partículas
    AMBIENT_PARTICLE_SIZE_MAX: float = 2.5         # Tamanho máximo das partículas
    AMBIENT_PARTICLE_LIFETIME_MIN: float = 8.0     # Tempo de vida mínimo
    AMBIENT_PARTICLE_LIFETIME_MAX: float = 20.0    # Tempo de vida máximo
    
    # === UI MODERNA ===
    UI_CORNER_RADIUS: int = 8                      # Raio das bordas arredondadas
    UI_PADDING: int = 12                           # Espaçamento interno dos painéis
    UI_SHADOW_INTENSITY: int = 80                  # Intensidade das sombras da UI
    UI_BREATH_AMPLITUDE: float = 0.02              # Amplitude da respiração da UI
    UI_BREATH_SPEED: float = 2.0                   # Velocidade da respiração da UI
    
    # === GRADIENTES E BRILHOS ===
    GRADIENT_STEPS: int = 50                       # Passos nos gradientes (performance)
    GLOW_LAYERS: int = 4                          # Camadas de brilho
    GLOW_FADE_FACTOR: float = 0.6                 # Fator de fade entre camadas
    
    # === PERFORMANCE E OTIMIZAÇÃO ===
    MAX_PARTICLES: int = 30                       # Máximo absoluto de partículas
    PARTICLE_SPAWN_INTERVAL: float = 0.5          # Intervalo entre spawn de partículas
    CACHE_SURFACES: bool = True                   # Se deve cachear superfícies
    USE_HARDWARE_ACCELERATION: bool = True        # Usar aceleração de hardware se disponível

# =============================================================================
# CONFIGURAÇÕES DE FONTES v3.0
# =============================================================================
class FontSizes:
    """Tamanhos de fontes otimizados para a nova UI"""
    TINY: int = 16
    SMALL: int = 24
    MEDIUM: int = 36
    LARGE: int = 48
    EXTRA_LARGE: int = 72
    MASSIVE: int = 96         # Para títulos especiais

# =============================================================================
# CONFIGURAÇÕES DE CONTROLES (Mantidas)
# =============================================================================
class Controls:
    """Mapeamento de controles do jogo (inalterado)"""
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
# CONFIGURAÇÕES DE POSIÇÕES INICIAIS (Mantidas)
# =============================================================================
INITIAL_SNAKE_X: int = GRID_WIDTH // 2
INITIAL_SNAKE_Y: int = GRID_HEIGHT // 2

# =============================================================================
# MENSAGENS DO JOGO v3.0
# =============================================================================
class Messages:
    """Mensagens exibidas no jogo com texto atualizado"""
    # Game states
    GAME_OVER: str = "GAME OVER"
    RESTART_INSTRUCTION: str = "Press R to restart or Q to quit"
    FINAL_SCORE: str = "Final Score: {score:,}"
    LEVEL_UP: str = "LEVEL UP!"
    PAUSED: str = "PAUSED - Press SPACE to continue"
    
    # HUD
    CURRENT_SCORE: str = "Score: {score:,}"
    SNAKE_LENGTH: str = "Length: {length}"
    CURRENT_LEVEL: str = "Level: {level}"
    SPEED_INFO: str = "Speed: {speed:.1f}x"
    
    # Novos para v3.0
    WELCOME_TITLE: str = "Snake Game v3.0"
    WELCOME_SUBTITLE: str = "Gruvbox Edition"
    SPECIAL_FOODS_TITLE: str = "Special Foods"
    
    # Estatísticas
    STATS_NORMAL: str = "🍎 Normal: {count}"
    STATS_SPECIAL: str = "⭐ Gold: {count}"
    STATS_FUGITIVE: str = "🏃‍♀️ Runner: {count}"
    STATS_MIRROR: str = "🪞 Mirror: {count}"

# =============================================================================
# CONFIGURAÇÕES DE DESENVOLVIMENTO E DEBUG
# =============================================================================
class Debug:
    """Configurações para desenvolvimento e debug"""
    SHOW_FPS: bool = False              # Mostrar FPS na tela
    SHOW_PARTICLE_COUNT: bool = False   # Mostrar contagem de partículas
    SHOW_GRID_COORDINATES: bool = False # Mostrar coordenadas do grid
    ENABLE_PERFORMANCE_PROFILING: bool = False  # Profiling de performance
    LOG_LEVEL: str = "INFO"             # Level de log (DEBUG, INFO, WARNING, ERROR)
    
    # Cores para elementos de debug
    DEBUG_TEXT_COLOR = Colors.BRIGHT_YELLOW
    DEBUG_OUTLINE_COLOR = Colors.BRIGHT_RED

# =============================================================================
# CONFIGURAÇÕES DE ÁUDIO (Preparação para futuras versões)
# =============================================================================
class Audio:
    """Configurações de áudio (preparado para v4.0)"""
    ENABLED: bool = False               # Áudio desabilitado por enquanto
    MASTER_VOLUME: float = 0.7          # Volume principal
    SFX_VOLUME: float = 0.8            # Volume dos efeitos sonoros
    MUSIC_VOLUME: float = 0.5          # Volume da música de fundo
    
    # Arquivos de som (para implementação futura)
    SOUND_EAT_NORMAL: str = "eat_normal.wav"
    SOUND_EAT_SPECIAL: str = "eat_special.wav"
    SOUND_GAME_OVER: str = "game_over.wav"
    SOUND_LEVEL_UP: str = "level_up.wav"

# =============================================================================
# METADADOS DO JOGO v3.0
# =============================================================================
class GameInfo:
    """Informações sobre o jogo"""
    VERSION: str = "3.0"
    CODENAME: str = "Gruvbox Edition"
    AUTHOR: str = "Snake Game Development Team"
    DESCRIPTION: str = "Modern Snake Game with Gruvbox theme and advanced graphics"
    
    # URLs (para futuras implementações)
    REPOSITORY_URL: str = "https://github.com/snake-game/gruvbox-edition"
    DOCUMENTATION_URL: str = "https://snake-game.github.io/docs"
    ISSUE_TRACKER_URL: str = "https://github.com/snake-game/gruvbox-edition/issues"

# =============================================================================
# VALIDAÇÃO E VERIFICAÇÕES
# =============================================================================
def validate_settings() -> bool:
    """
    Valida se todas as configurações estão corretas
    
    Returns:
        True se todas as configurações são válidas
    """
    try:
        # Verifica se o grid cabe na janela
        assert WINDOW_WIDTH > 0 and WINDOW_HEIGHT > 0
        assert GRID_SIZE > 0
        assert GRID_WIDTH > 10 and GRID_HEIGHT > 10
        
        # Verifica configurações de gameplay
        assert BASE_FPS > 0 and MAX_FPS > BASE_FPS
        assert FPS_INCREASE_PER_LEVEL > 1.0
        assert POINTS_PER_LEVEL > 0
        
        # Verifica probabilidades de spawn
        total_spawn_chance = (SPECIAL_FOOD_SPAWN_CHANCE + 
                            FUGITIVE_FOOD_SPAWN_CHANCE + 
                            MIRROR_FOOD_SPAWN_CHANCE)
        assert 0 < total_spawn_chance < 1.0
        
        # Verifica configurações visuais
        assert 0 <= Effects.GRID_TRANSPARENCY <= 255
        assert Effects.AMBIENT_PARTICLE_COUNT > 0
        assert Effects.UI_CORNER_RADIUS >= 0
        
        return True
        
    except AssertionError as e:
        print(f"❌ Erro na validação das configurações: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Erro inesperado na validação: {e}")
        return False

# =============================================================================
# INICIALIZAÇÃO AUTOMÁTICA
# =============================================================================
if __name__ == "__main__":
    # Executa validação quando arquivo é executado diretamente
    print("🔧 Validando configurações do Snake Game v3.0...")
    
    if validate_settings():
        print("✅ Todas as configurações estão válidas!")
        print(f"🎮 {GameInfo.VERSION} - {GameInfo.CODENAME}")
        print(f"📏 Janela: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"🔲 Grid: {GRID_WIDTH}x{GRID_HEIGHT} ({GRID_SIZE}px)")
        print(f"🎨 Tema: Gruvbox com {len(Colors.RAINBOW_COLORS)} cores do arco-íris")
        print(f"✨ Partículas: {Effects.AMBIENT_PARTICLE_COUNT} ambientais")
        print(f"🚀 Performance: {Effects.MAX_PARTICLES} partículas máximas")
    else:
        print("❌ Configurações inválidas detectadas!")
        exit(1)

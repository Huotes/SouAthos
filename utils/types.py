"""
Type hints personalizados para o Snake Game
Melhora a legibilidade e type safety
"""

from typing import Tuple, List, Callable, Optional, Protocol
import pygame

# =============================================================================
# TIPOS BÁSICOS
# =============================================================================
Position = Tuple[int, int]
Color = Tuple[int, int, int]
Size = Tuple[int, int]
SnakeBody = List[Position]

# =============================================================================
# TIPOS PARA PYGAME
# =============================================================================
Surface = pygame.Surface
Clock = pygame.time.Clock
Event = pygame.event.Event
Rect = pygame.Rect
Font = pygame.font.Font

# =============================================================================
# TIPOS FUNCIONAIS
# =============================================================================
EventHandler = Callable[[Event], None]
UpdateCallback = Callable[[], None]
RenderCallback = Callable[[Surface], None]

# =============================================================================
# PROTOCOLS (INTERFACES)
# =============================================================================
class Drawable(Protocol):
    """Protocol para objetos que podem ser desenhados"""
    def draw(self, surface: Surface) -> None:
        """Desenha o objeto na superfície"""
        ...

class Updatable(Protocol):
    """Protocol para objetos que podem ser atualizados"""
    def update(self) -> None:
        """Atualiza o estado do objeto"""
        ...

class Movable(Protocol):
    """Protocol para objetos que podem se mover"""
    def move(self) -> None:
        """Move o objeto"""
        ...
    
    @property
    def position(self) -> Position:
        """Posição atual do objeto"""
        ...

# =============================================================================
# TIPOS COMPOSTOS
# =============================================================================
GameObjectData = dict
CollisionInfo = Tuple[bool, Optional[str]]

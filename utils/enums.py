"""
Enumerações utilizadas no Snake Game
Princípio KISS: Definições simples e claras
"""

from enum import Enum
from typing import Tuple

class Direction(Enum):
    """Direções de movimento da cobra"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    @property
    def opposite(self) -> 'Direction':
        """Retorna a direção oposta"""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return opposites[self]
    
    @property
    def delta(self) -> Tuple[int, int]:
        """Retorna o delta x,y da direção"""
        return self.value

class GameState(Enum):
    """Estados possíveis do jogo"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    QUIT = "quit"

class EntityType(Enum):
    """Tipos de entidades do jogo"""
    SNAKE_HEAD = "snake_head"
    SNAKE_BODY = "snake_body" 
    FOOD_NORMAL = "food_normal"
    FOOD_SPECIAL = "food_special"
    FOOD_FUGITIVE = "food_fugitive"
    TRAIL_PARTICLE = "trail_particle"

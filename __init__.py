# core/__init__.py
"""
Módulo core - Sistema principal do jogo
Contém o engine e gerenciadores de eventos
"""

from .game_engine import GameEngine
from .events import EventManager, GameEventDispatcher, game_events

__all__ = [
    'GameEngine',
    'EventManager', 
    'GameEventDispatcher',
    'game_events'
]

# entities/__init__.py
"""
Módulo entities - Objetos do jogo
Contém todas as entidades que podem ser desenhadas e atualizadas
"""

from .game_object import GameObject
from .snake import Snake
from .food import Food, SpecialFood, FugitiveFood, TrailParticle
from .food_manager import FoodManager

__all__ = [
    'GameObject',
    'Snake', 
    'Food',
    'SpecialFood',
    'FugitiveFood',
    'TrailParticle',
    'FoodManager'
]

# graphics/__init__.py
"""
Módulo graphics - Sistema de renderização
Contém o renderer e gerenciador de UI
"""

from .renderer import Renderer
from .ui import UIManager

__all__ = [
    'Renderer',
    'UIManager'
]

# utils/__init__.py
"""
Módulo utils - Utilitários compartilhados
Contém enums, types e funções auxiliares
"""

from .enums import Direction, GameState, EntityType
from .types import Position, Color, Size, SnakeBody

__all__ = [
    'Direction',
    'GameState', 
    'EntityType',
    'Position',
    'Color',
    'Size',
    'SnakeBody'
]

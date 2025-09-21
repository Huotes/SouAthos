"""
Classe base abstrata para objetos do jogo
Princípio POO: Herança e abstração
"""

from abc import ABC, abstractmethod
import pygame
from utils.types import Surface, Position, Color
from utils.enums import EntityType

class GameObject(ABC):
    """
    Classe base abstrata para todos os objetos do jogo
    
    Princípios aplicados:
    - Abstração: Define interface comum
    - Encapsulamento: Propriedades protegidas
    - Polimorfismo: Métodos abstratos implementados pelas subclasses
    """
    
    def __init__(self, position: Position, entity_type: EntityType):
        """
        Inicializa um objeto do jogo
        
        Args:
            position: Posição inicial (x, y)
            entity_type: Tipo da entidade
        """
        self._position = position
        self._entity_type = entity_type
        self._active = True
    
    @property
    def position(self) -> Position:
        """Retorna a posição atual do objeto"""
        return self._position
    
    @position.setter 
    def position(self, new_position: Position) -> None:
        """Define nova posição do objeto"""
        self._position = new_position
    
    @property
    def entity_type(self) -> EntityType:
        """Retorna o tipo da entidade"""
        return self._entity_type
    
    @property
    def active(self) -> bool:
        """Retorna se o objeto está ativo"""
        return self._active
    
    def activate(self) -> None:
        """Ativa o objeto"""
        self._active = True
    
    def deactivate(self) -> None:
        """Desativa o objeto"""
        self._active = False
    
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        """
        Desenha o objeto na superfície (método abstrato)
        
        Args:
            surface: Superfície onde desenhar
        """
        pass
    
    @abstractmethod
    def get_bounds(self) -> pygame.Rect:
        """
        Retorna os limites do objeto para detecção de colisão
        
        Returns:
            Retângulo representando os limites
        """
        pass
    
    def collides_with(self, other: 'GameObject') -> bool:
        """
        Verifica colisão com outro objeto
        
        Args:
            other: Outro objeto para verificar colisão
            
        Returns:
            True se houver colisão, False caso contrário
        """
        if not self.active or not other.active:
            return False
        
        return self.get_bounds().colliderect(other.get_bounds())
    
    def __repr__(self) -> str:
        """Representação em string do objeto"""
        return f"{self.__class__.__name__}(position={self.position}, type={self.entity_type})"

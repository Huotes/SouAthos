"""
Classe Snake refatorada com herança e boas práticas
Princípios POO: Herança, encapsulamento, responsabilidade única
"""

import pygame
from typing import List
from entities.game_object import GameObject
from utils.types import Position, Surface, SnakeBody
from utils.enums import Direction, EntityType
from config.settings import GRID_SIZE, Colors, GRID_WIDTH, GRID_HEIGHT

class Snake(GameObject):
    """
    Classe representando a cobra do jogo
    
    Responsabilidades:
    - Movimento da cobra
    - Crescimento
    - Detecção de colisões próprias
    - Renderização
    """
    
    def __init__(self, initial_position: Position):
        """
        Inicializa a cobra
        
        Args:
            initial_position: Posição inicial da cabeça
        """
        super().__init__(initial_position, EntityType.SNAKE_HEAD)
        self._body: SnakeBody = [initial_position]
        self._direction = Direction.RIGHT
        self._next_direction = Direction.RIGHT
        self._should_grow = False
    
    @property
    def body(self) -> SnakeBody:
        """Retorna o corpo da cobra"""
        return self._body.copy()
    
    @property
    def head_position(self) -> Position:
        """Retorna a posição da cabeça"""
        return self._body[0]
    
    @property
    def length(self) -> int:
        """Retorna o comprimento da cobra"""
        return len(self._body)
    
    @property
    def direction(self) -> Direction:
        """Retorna a direção atual"""
        return self._direction
    
    def change_direction(self, new_direction: Direction) -> None:
        """
        Muda a direção da cobra (evita direção oposta)
        
        Args:
            new_direction: Nova direção desejada
        """
        if new_direction != self._direction.opposite:
            self._next_direction = new_direction
    
    def grow(self) -> None:
        """Marca a cobra para crescer na próxima movimentação"""
        self._should_grow = True
    
    def move(self) -> None:
        """Move a cobra na direção atual"""
        if not self.active:
            return
        
        # Atualiza direção se necessário
        self._direction = self._next_direction
        
        # Calcula nova posição da cabeça
        head_x, head_y = self.head_position
        dx, dy = self._direction.delta
        new_head = (head_x + dx, head_y + dy)
        
        # Adiciona nova cabeça
        self._body.insert(0, new_head)
        self._position = new_head
        
        # Remove cauda se não deve crescer
        if not self._should_grow:
            self._body.pop()
        else:
            self._should_grow = False
    
    def check_self_collision(self) -> bool:
        """
        Verifica se a cobra colidiu consigo mesma
        
        Returns:
            True se houve colisão consigo mesma
        """
        return self.head_position in self._body[1:]
    
    def check_wall_collision(self) -> bool:
        """
        Verifica se a cobra colidiu com as paredes
        
        Returns:
            True se houve colisão com parede
        """
        head_x, head_y = self.head_position
        return (head_x < 0 or head_x >= GRID_WIDTH or 
                head_y < 0 or head_y >= GRID_HEIGHT)
    
    def reset(self, initial_position: Position) -> None:
        """
        Reseta a cobra para o estado inicial
        
        Args:
            initial_position: Nova posição inicial
        """
        self._position = initial_position
        self._body = [initial_position]
        self._direction = Direction.RIGHT
        self._next_direction = Direction.RIGHT
        self._should_grow = False
        self.activate()
    
    def draw(self, surface: Surface) -> None:
        """
        Desenha a cobra na superfície
        
        Args:
            surface: Superfície onde desenhar
        """
        if not self.active:
            return
        
        for i, segment in enumerate(self._body):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Desenha cabeça com cor diferente
            if i == 0:
                pygame.draw.rect(surface, Colors.DARK_GREEN, rect)
                # Adiciona "olhos" na cabeça
                eye_size = GRID_SIZE // 6
                eye_offset = GRID_SIZE // 4
                
                left_eye = pygame.Rect(
                    x * GRID_SIZE + eye_offset,
                    y * GRID_SIZE + eye_offset,
                    eye_size, eye_size
                )
                right_eye = pygame.Rect(
                    x * GRID_SIZE + GRID_SIZE - eye_offset - eye_size,
                    y * GRID_SIZE + eye_offset,
                    eye_size, eye_size
                )
                
                pygame.draw.rect(surface, Colors.WHITE, left_eye)
                pygame.draw.rect(surface, Colors.WHITE, right_eye)
            else:
                # Corpo com gradiente sutil
                color_intensity = max(100, 255 - (i * 10))
                body_color = (0, min(255, color_intensity), 0)
                pygame.draw.rect(surface, body_color, rect)
            
            # Borda dos segmentos
            pygame.draw.rect(surface, Colors.BLACK, rect, 1)
    
    def get_bounds(self) -> pygame.Rect:
        """
        Retorna os limites da cabeça para detecção de colisão
        
        Returns:
            Retângulo da cabeça
        """
        x, y = self.head_position
        return pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

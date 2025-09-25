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
        Desenha a cobra com visual Gruvbox moderno
        
        Args:
            surface: Superfície onde desenhar
        """
        if not self.active:
            return
        
        for i, segment in enumerate(self._body):
            x, y = segment
            center_x = x * GRID_SIZE + GRID_SIZE // 2
            center_y = y * GRID_SIZE + GRID_SIZE // 2
            
            if i == 0:  # Cabeça
                # Sombra da cabeça
                shadow_offset = 2
                shadow_surface = pygame.Surface((GRID_SIZE + 4, GRID_SIZE + 4))
                shadow_surface.set_alpha(100)
                shadow_surface.set_colorkey(Colors.BLACK)
                pygame.draw.circle(shadow_surface, Colors.SHADOW_COLOR, 
                                 ((GRID_SIZE + 4) // 2, (GRID_SIZE + 4) // 2), 
                                 GRID_SIZE // 2)
                surface.blit(shadow_surface, 
                           (center_x - GRID_SIZE // 2 + shadow_offset - 2, 
                            center_y - GRID_SIZE // 2 + shadow_offset - 2))
                
                # Gradiente da cabeça (verde brilhante Gruvbox)
                head_radius = GRID_SIZE // 2 - 1
                
                # Brilho externo
                for glow_radius in range(head_radius + 6, head_radius, -1):
                    alpha = max(0, 30 - (glow_radius - head_radius) * 5)
                    if alpha > 0:
                        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2))
                        glow_surface.set_alpha(alpha)
                        glow_surface.set_colorkey(Colors.BLACK)
                        pygame.draw.circle(glow_surface, Colors.SNAKE_HEAD, 
                                         (glow_radius, glow_radius), glow_radius)
                        surface.blit(glow_surface, 
                                   (center_x - glow_radius, center_y - glow_radius))
                
                # Cabeça principal com gradiente
                pygame.draw.circle(surface, Colors.SNAKE_HEAD, (center_x, center_y), head_radius)
                
                # Círculo interno mais claro
                inner_radius = head_radius - 2
                if inner_radius > 0:
                    pygame.draw.circle(surface, Colors.BRIGHT_GREEN, 
                                     (center_x, center_y), inner_radius)
                
                # Olhos com tema Gruvbox
                eye_size = max(2, GRID_SIZE // 8)
                eye_offset_x = GRID_SIZE // 4
                eye_offset_y = GRID_SIZE // 6
                
                # Olho esquerdo
                left_eye_x = center_x - eye_offset_x
                left_eye_y = center_y - eye_offset_y
                pygame.draw.circle(surface, Colors.FG_LIGHT, (left_eye_x, left_eye_y), eye_size)
                pygame.draw.circle(surface, Colors.BG_DARK, (left_eye_x, left_eye_y), eye_size - 1)
                
                # Olho direito
                right_eye_x = center_x + eye_offset_x
                right_eye_y = center_y - eye_offset_y
                pygame.draw.circle(surface, Colors.FG_LIGHT, (right_eye_x, right_eye_y), eye_size)
                pygame.draw.circle(surface, Colors.BG_DARK, (right_eye_x, right_eye_y), eye_size - 1)
                
                # Borda da cabeça
                pygame.draw.circle(surface, Colors.BG_DARK, (center_x, center_y), head_radius, 2)
                
            else:  # Corpo
                # Sombra do corpo
                shadow_surface = pygame.Surface((GRID_SIZE + 2, GRID_SIZE + 2))
                shadow_surface.set_alpha(80 - i * 5)  # Sombra diminui com distância
                shadow_surface.set_colorkey(Colors.BLACK)
                pygame.draw.circle(shadow_surface, Colors.SHADOW_COLOR, 
                                 ((GRID_SIZE + 2) // 2, (GRID_SIZE + 2) // 2), 
                                 GRID_SIZE // 2 - 1)
                surface.blit(shadow_surface, 
                           (center_x - GRID_SIZE // 2 + 1 - 1, 
                            center_y - GRID_SIZE // 2 + 1 - 1))
                
                # Cor do corpo com gradiente baseado na posição
                segment_intensity = max(0.6, 1.0 - (i * 0.05))  # Gradiente mais sutil
                body_color = tuple(int(c * segment_intensity) for c in Colors.SNAKE_BODY)
                
                body_radius = GRID_SIZE // 2 - 2
                
                # Corpo principal
                pygame.draw.circle(surface, body_color, (center_x, center_y), body_radius)
                
                # Highlight interno
                inner_color = tuple(min(255, int(c * 1.2)) for c in body_color)
                inner_radius = body_radius - 2
                if inner_radius > 0:
                    pygame.draw.circle(surface, inner_color, (center_x, center_y), inner_radius)
                
                # Borda sutil
                pygame.draw.circle(surface, Colors.BG_DARK, (center_x, center_y), body_radius, 1)
    
    def get_bounds(self) -> pygame.Rect:
        """
        Retorna os limites da cabeça para detecção de colisão
        
        Returns:
            Retângulo da cabeça
        """
        x, y = self.head_position
        return pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

"""
Sistema de renderização centralizado
Princípio DRY: Evita duplicação de código de desenho
Responsabilidade única: Apenas renderização
Inclui sistema de grid transparente e efeitos visuais
"""

import pygame
import math
from typing import List, Optional
from utils.types import Surface, Color
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, 
    Colors, WINDOW_TITLE, Effects
)

class Renderer:
    """
    Sistema centralizado de renderização
    
    Responsabilidades:
    - Inicialização da janela
    - Renderização de primitivas
    - Controle do display
    - Renderização do grid
    """
    
    def __init__(self):
        """Inicializa o sistema de renderização"""
        pygame.display.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self._background_color = Colors.BLACK
        
        # Superfície para grid transparente
        self._grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._grid_surface.set_alpha(Effects.GRID_TRANSPARENCY)
        self._grid_surface.set_colorkey(Colors.BLACK)  # Fundo transparente
        
        # Efeito de level up
        self._level_up_timer = 0.0
        self._level_up_active = False
        
        # Efeito espelho
        self._mirror_effect_timer = 0.0
        self._mirror_effect_active = False
        self._screen_flash_timer = 0.0
        self._screen_flash_active = False
    
    @property
    def screen(self) -> Surface:
        """Retorna a superfície da tela principal"""
        return self._screen
    
    def clear_screen(self, color: Optional[Color] = None) -> None:
        """
        Limpa a tela com uma cor
        
        Args:
            color: Cor para limpar (usa cor de fundo se None)
        """
        fill_color = color if color else self._background_color
        self._screen.fill(fill_color)
    
    def draw_grid(self, line_color: Color = Colors.GRAY, line_width: int = 1) -> None:
        """
        Desenha o grid de fundo com transparência
        
        Args:
            line_color: Cor das linhas do grid
            line_width: Espessura das linhas
        """
        # Limpa a superfície do grid
        self._grid_surface.fill(Colors.BLACK)
        
        # Escolhe a cor baseada no efeito de level up
        if self._level_up_active:
            # Calcula cor do arco-íris baseado no tempo
            color_index = int((self._level_up_timer * 10) % len(Colors.RAINBOW_COLORS))
            actual_color = Colors.RAINBOW_COLORS[color_index]
            # Intensidade pulsante
            intensity = 0.5 + 0.5 * abs(math.sin(self._level_up_timer * 8))
            actual_color = tuple(int(c * intensity) for c in actual_color)
        else:
            actual_color = line_color
        
        # Linhas verticais
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(
                self._grid_surface, 
                actual_color, 
                (x, 0), 
                (x, WINDOW_HEIGHT), 
                line_width
            )
        
        # Linhas horizontais
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(
                self._grid_surface, 
                actual_color, 
                (0, y), 
                (WINDOW_WIDTH, y), 
                line_width
            )
        
        # Desenha o grid transparente na tela
        self._screen.blit(self._grid_surface, (0, 0))
    
    def draw_rect(self, color: Color, rect: pygame.Rect, width: int = 0) -> None:
        """
        Desenha um retângulo
        
        Args:
            color: Cor do retângulo
            rect: Retângulo a ser desenhado
            width: Espessura da borda (0 = preenchido)
        """
        pygame.draw.rect(self._screen, color, rect, width)
    
    def draw_circle(self, color: Color, center: tuple, radius: int, width: int = 0) -> None:
        """
        Desenha um círculo
        
        Args:
            color: Cor do círculo
            center: Centro (x, y)
            radius: Raio
            width: Espessura da borda (0 = preenchido)
        """
        pygame.draw.circle(self._screen, color, center, radius, width)
    
    def draw_line(self, color: Color, start_pos: tuple, end_pos: tuple, width: int = 1) -> None:
        """
        Desenha uma linha
        
        Args:
            color: Cor da linha
            start_pos: Posição inicial (x, y)
            end_pos: Posição final (x, y)
            width: Espessura da linha
        """
        pygame.draw.line(self._screen, color, start_pos, end_pos, width)
    
    def draw_polygon(self, color: Color, points: List[tuple], width: int = 0) -> None:
        """
        Desenha um polígono
        
        Args:
            color: Cor do polígono
            points: Lista de pontos [(x, y), ...]
            width: Espessura da borda (0 = preenchido)
        """
        if len(points) >= 3:
            pygame.draw.polygon(self._screen, color, points, width)
    
    def present(self) -> None:
        """Atualiza o display"""
        pygame.display.flip()
    
    def set_background_color(self, color: Color) -> None:
        """
        Define a cor de fundo
        
        Args:
            color: Nova cor de fundo
        """
        self._background_color = color
    
    def get_screen_size(self) -> tuple:
        """
        Retorna o tamanho da tela
        
        Returns:
            Tupla (largura, altura)
        """
        return (WINDOW_WIDTH, WINDOW_HEIGHT)
    
    def cleanup(self) -> None:
        """Limpa recursos do renderer"""
        pygame.display.quit()
    
    def start_level_up_effect(self) -> None:
        """Inicia o efeito visual de level up"""
        self._level_up_active = True
        self._level_up_timer = 0.0
        print("🌈 Efeito de level up ativado!")
    
    def update_effects(self, delta_time: float) -> None:
        """
        Atualiza efeitos visuais
        
        Args:
            delta_time: Tempo decorrido desde a última atualização
        """
        if self._level_up_active:
            self._level_up_timer += delta_time
            
            # Para o efeito após a duração configurada
            if self._level_up_timer >= Effects.LEVEL_UP_FLASH_DURATION:
                self._level_up_active = False
                self._level_up_timer = 0.0
                print("✨ Efeito de level up finalizado")
    
    def start_mirror_effect(self) -> None:
        """Inicia o efeito visual de espelho"""
        self._mirror_effect_active = True
        self._mirror_effect_timer = 0.0
        print("🪞 Efeito de espelhamento ativado!")
    
    def start_screen_flash(self, color: tuple = (255, 255, 255)) -> None:
        """Inicia efeito de flash na tela"""
        self._screen_flash_active = True
        self._screen_flash_timer = 0.0
        self._flash_color = color
        print(f"⚡ Flash da tela ativado com cor {color}!")
        """
        Verifica se o efeito de level up está ativo
        
        Returns:
            True se efeito ativo, False caso contrário
        """
        return self._level_up_active
    
    def is_mirror_effect_active(self) -> bool:
        """
        Verifica se o efeito de espelho está ativo
        
        Returns:
            True se efeito ativo
        """
        return self._mirror_effect_active
    
    def apply_mirror_transform(self, surface: Surface) -> None:
        """
        Aplica transformação de espelhamento na superfície
        
        Args:
            surface: Superfície a ser espelhada
        """
        if self._mirror_effect_active:
            # Cria uma superfície espelhada horizontalmente
            flipped_surface = pygame.transform.flip(surface, True, False)
            
            # Calcula intensidade do efeito baseado no tempo
            effect_progress = self._mirror_effect_timer / Effects.MIRROR_EFFECT_DURATION
            alpha = int(255 * (1.0 - effect_progress))  # Desvanece gradualmente
            
            # Aplica transparência
            flipped_surface.set_alpha(alpha)
            
            # Desenha sobre a superfície original
            surface.blit(flipped_surface, (0, 0))
    
    def apply_screen_flash(self, surface: Surface) -> None:
        """
        Aplica efeito de flash na tela
        
        Args:
            surface: Superfície onde aplicar o flash
        """
        if self._screen_flash_active:
            # Calcula intensidade baseado no tempo
            progress = self._screen_flash_timer / Effects.SPECIAL_CONSUME_EFFECT_DURATION
            intensity = int(Effects.SCREEN_FLASH_INTENSITY * (1.0 - progress))
            
            if intensity > 0:
                # Cria overlay de flash
                flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                flash_surface.set_alpha(intensity)
                flash_surface.fill(getattr(self, '_flash_color', (255, 255, 255)))
                
                # Aplica na tela
                surface.blit(flash_surface, (0, 0))

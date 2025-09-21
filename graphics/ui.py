"""
Sistema de interface do usuário
Princípio de responsabilidade única: Apenas UI
"""

import pygame
from typing import Optional, Tuple
from utils.types import Surface, Color, Font
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, Colors, 
    FontSizes, Messages
)

class UIManager:
    """
    Gerenciador da interface do usuário
    
    Responsabilidades:
    - Renderização de texto
    - Posicionamento de elementos
    - Gerenciamento de fontes
    """
    
    def __init__(self):
        """Inicializa o gerenciador de UI"""
        pygame.font.init()
        self._fonts = {
            'small': pygame.font.Font(None, FontSizes.SMALL),
            'medium': pygame.font.Font(None, FontSizes.MEDIUM),
            'large': pygame.font.Font(None, FontSizes.LARGE),
            'extra_large': pygame.font.Font(None, FontSizes.EXTRA_LARGE)
        }
    
    def get_font(self, size: str) -> Font:
        """
        Retorna uma fonte pelo tamanho
        
        Args:
            size: Tamanho da fonte ('small', 'medium', 'large', 'extra_large')
            
        Returns:
            Objeto Font
        """
        return self._fonts.get(size, self._fonts['medium'])
    
    def render_text(self, text: str, font_size: str = 'medium', 
                   color: Color = Colors.WHITE, 
                   antialias: bool = True) -> Surface:
        """
        Renderiza texto em uma superfície
        
        Args:
            text: Texto a ser renderizado
            font_size: Tamanho da fonte
            color: Cor do texto
            antialias: Usar antialiasing
            
        Returns:
            Superfície com o texto renderizado
        """
        font = self.get_font(font_size)
        return font.render(text, antialias, color)
    
    def draw_text_centered(self, surface: Surface, text: str, 
                          position: Tuple[int, int], font_size: str = 'medium',
                          color: Color = Colors.WHITE) -> pygame.Rect:
        """
        Desenha texto centralizado em uma posição
        
        Args:
            surface: Superfície onde desenhar
            text: Texto a desenhar
            position: Posição central (x, y)
            font_size: Tamanho da fonte
            color: Cor do texto
            
        Returns:
            Retângulo ocupado pelo texto
        """
        text_surface = self.render_text(text, font_size, color)
        text_rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, text_rect)
        return text_rect
    
    def draw_text_at(self, surface: Surface, text: str, 
                    position: Tuple[int, int], font_size: str = 'medium',
                    color: Color = Colors.WHITE) -> pygame.Rect:
        """
        Desenha texto em uma posição específica (canto superior esquerdo)
        
        Args:
            surface: Superfície onde desenhar
            text: Texto a desenhar
            position: Posição (x, y)
            font_size: Tamanho da fonte
            color: Cor do texto
            
        Returns:
            Retângulo ocupado pelo texto
        """
        text_surface = self.render_text(text, font_size, color)
        text_rect = text_surface.get_rect(topleft=position)
        surface.blit(text_surface, text_rect)
        return text_rect
    
    def get_text_size(self, text: str, font_size: str = 'medium') -> Tuple[int, int]:
        """
        Retorna o tamanho de um texto
        
        Args:
            text: Texto a medir
            font_size: Tamanho da fonte
            
        Returns:
            Tupla (largura, altura)
        """
        font = self.get_font(font_size)
        return font.size(text)
    
    def draw_hud(self, surface: Surface, score: int, length: int, 
                level: int = 1, speed_multiplier: float = 1.0, 
                food_stats: dict = None) -> None:
        """
        Desenha o HUD (heads-up display) do jogo
        
        Args:
            surface: Superfície onde desenhar
            score: Pontuação atual
            length: Tamanho da cobra
            level: Nível atual
            speed_multiplier: Multiplicador de velocidade
            food_stats: Estatísticas de comidas (opcional)
        """
        # Score
        score_text = Messages.CURRENT_SCORE.format(score=score)
        self.draw_text_at(surface, score_text, (10, 10), 'medium', Colors.WHITE)
        
        # Tamanho da cobra
        length_text = Messages.SNAKE_LENGTH.format(length=length)
        self.draw_text_at(surface, length_text, (10, 50), 'medium', Colors.WHITE)
        
        # Nível (com destaque)
        level_text = Messages.CURRENT_LEVEL.format(level=level)
        level_color = Colors.WHITE if level == 1 else (255, 215, 0)  # Dourado para níveis > 1
        self.draw_text_at(surface, level_text, (10, 90), 'medium', level_color)
        
        # Velocidade (lado direito)
        speed_text = Messages.SPEED_INFO.format(speed=speed_multiplier)
        speed_color = (255, 100, 100) if speed_multiplier > 2 else Colors.LIGHT_GRAY
        text_width, _ = self.get_text_size(speed_text, 'small')
        self.draw_text_at(surface, speed_text, 
                         (WINDOW_WIDTH - text_width - 10, 10), 
                         'small', speed_color)
        
        # Legenda das comidas especiais (canto superior direito)
        if food_stats:
            legend_x = WINDOW_WIDTH - 200
            legend_y = 50
            
            # Comida especial
            if food_stats.get('special_consumed', 0) > 0:
                special_text = f"⭐ Especiais: {food_stats['special_consumed']}"
                self.draw_text_at(surface, special_text, 
                                (legend_x, legend_y), 'small', Colors.SPECIAL_FOOD_COLOR)
                legend_y += 20
            
            # Comida fugitiva
            if food_stats.get('fugitive_consumed', 0) > 0:
                fugitive_text = f"🏃‍♀️ Fugitivas: {food_stats['fugitive_consumed']}"
                self.draw_text_at(surface, fugitive_text, 
                                (legend_x, legend_y), 'small', Colors.FUGITIVE_FOOD_COLOR)
                legend_y += 20
            
            # Fugas
            if food_stats.get('fugitive_escapes', 0) > 0:
                escapes_text = f"💨 Fugas: {food_stats['fugitive_escapes']}"
                self.draw_text_at(surface, escapes_text, 
                                (legend_x, legend_y), 'small', Colors.GRAY)
    
    def draw_game_over_screen(self, surface: Surface, final_score: int) -> None:
        """
        Desenha a tela de game over
        
        Args:
            surface: Superfície onde desenhar
            final_score: Pontuação final
        """
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Fundo semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        surface.blit(overlay, (0, 0))
        
        # Game Over
        self.draw_text_centered(
            surface, Messages.GAME_OVER, 
            (center_x, center_y - 80), 
            'extra_large', Colors.RED
        )
        
        # Score final
        final_score_text = Messages.FINAL_SCORE.format(score=final_score)
        self.draw_text_centered(
            surface, final_score_text, 
            (center_x, center_y - 20), 
            'large', Colors.WHITE
        )
        
        # Instruções
        self.draw_text_centered(
            surface, Messages.RESTART_INSTRUCTION, 
            (center_x, center_y + 40), 
            'medium', Colors.LIGHT_GRAY
        )
    
    def draw_pause_screen(self, surface: Surface) -> None:
        """
        Desenha a tela de pausa
        
        Args:
            surface: Superfície onde desenhar
        """
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Fundo semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(Colors.BLACK)
        surface.blit(overlay, (0, 0))
        
        # Texto de pausa
        self.draw_text_centered(
            surface, Messages.PAUSED,
            (center_x, center_y),
            'large', Colors.WHITE
        )
    
    def draw_menu(self, surface: Surface, title: str, options: list, 
                 selected_index: int = 0) -> None:
        """
        Desenha um menu simples
        
        Args:
            surface: Superfície onde desenhar
            title: Título do menu
            options: Lista de opções
            selected_index: Índice da opção selecionada
        """
        center_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2 - 100
        
        # Título
        self.draw_text_centered(
            surface, title,
            (center_x, start_y),
            'large', Colors.WHITE
        )
        
        # Opções
        for i, option in enumerate(options):
            y_pos = start_y + 80 + (i * 50)
            color = Colors.WHITE if i == selected_index else Colors.GRAY
            
            self.draw_text_centered(
                surface, option,
                (center_x, y_pos),
                'medium', color
            )
            
            # Indicador de seleção
            if i == selected_index:
                self.draw_text_centered(
                    surface, "> ",
                    (center_x - 100, y_pos),
                    'medium', Colors.WHITE
                )
    
    def cleanup(self) -> None:
        """Limpa recursos da UI"""
        pygame.font.quit()
    
    def draw_level_up_notification(self, surface: Surface, level: int) -> None:
        """
        Desenha notificação de level up
        
        Args:
            surface: Superfície onde desenhar
            level: Novo nível alcançado
        """
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2 - 150
        
        # Fundo semi-transparente colorido
        overlay = pygame.Surface((400, 100))
        overlay.set_alpha(180)
        
        # Cor de fundo baseada no nível (ciclo de cores)
        bg_color_index = (level - 1) % len(Colors.RAINBOW_COLORS)
        bg_color = Colors.RAINBOW_COLORS[bg_color_index]
        overlay.fill(bg_color)
        
        overlay_rect = overlay.get_rect(center=(center_x, center_y))
        surface.blit(overlay, overlay_rect)
        
        # Texto "LEVEL UP!"
        self.draw_text_centered(
            surface, Messages.LEVEL_UP,
            (center_x, center_y - 20),
            'large', Colors.WHITE
        )
        
        # Número do nível
        level_text = f"Nível {level}"
        self.draw_text_centered(
            surface, level_text,
            (center_x, center_y + 20),
            'medium', Colors.WHITE
        )

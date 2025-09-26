"""
Sistema de interface moderna com tema Gruvbox
Inclui elementos animados, bordas arredondadas e gradientes
"""

import pygame
import math
from typing import Optional, Tuple, List
from utils.types import Surface, Color, Font
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PLAY_AREA_HEIGHT, PLAY_AREA_WIDTH, Colors, 
    FontSizes, Messages, Effects
)

class UIManager:
    """
    Gerenciador de interface moderna com tema Gruvbox
    
    Recursos:
    - Painéis com bordas arredondadas
    - Gradientes suaves
    - Animações fluidas
    - Sombras realistas
    - Tema Gruvbox consistente
    """
    
    def __init__(self):
        """Inicializa o gerenciador de UI moderna"""
        pygame.font.init()
        
        # Carrega fontes com melhor qualidade
        self._fonts = {
            'small': pygame.font.Font(None, FontSizes.SMALL),
            'medium': pygame.font.Font(None, FontSizes.MEDIUM),
            'large': pygame.font.Font(None, FontSizes.LARGE),
            'extra_large': pygame.font.Font(None, FontSizes.EXTRA_LARGE)
        }
        
        # Timer para animações da UI
        self._animation_timer = 0.0
        
        # Cache de superfícies renderizadas
        self._text_cache = {}
        
        print("🎨 ModernUIManager inicializado com tema Gruvbox!")
    
    def update_animations(self, delta_time: float) -> None:
        """Atualiza animações da UI"""
        self._animation_timer += delta_time
    
    def get_font(self, size: str) -> Font:
        """Retorna fonte pelo tamanho"""
        return self._fonts.get(size, self._fonts['medium'])
    
    def _create_rounded_surface(self, size: Tuple[int, int], color: Color, 
                               radius: int = Effects.UI_CORNER_RADIUS,
                               border_color: Optional[Color] = None,
                               border_width: int = 0) -> Surface:
        """
        Cria superfície com bordas arredondadas
        
        Args:
            size: Tamanho da superfície
            color: Cor de preenchimento
            radius: Raio das bordas
            border_color: Cor da borda
            border_width: Espessura da borda
        """
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparente
        
        # Retângulo com bordas arredondadas
        pygame.draw.rect(surface, color, (0, 0, *size), border_radius=radius)
        
        if border_color and border_width > 0:
            pygame.draw.rect(surface, border_color, (0, 0, *size), 
                           border_width, border_radius=radius)
        
        return surface
    
    def _draw_shadow(self, surface: Surface, rect: pygame.Rect, 
                    intensity: int = Effects.UI_SHADOW_INTENSITY) -> None:
        """Desenha sombra suave para elementos da UI"""
        shadow_rect = rect.move(3, 3)
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((*Colors.SHADOW_COLOR, intensity))
        
        # Blur simples com múltiplas camadas
        for i in range(3):
            blur_rect = shadow_rect.move(-i, -i)
            blur_alpha = intensity // (i + 2)
            blur_surface = pygame.Surface((blur_rect.width + i*2, blur_rect.height + i*2), pygame.SRCALPHA)
            blur_surface.fill((*Colors.SHADOW_COLOR, blur_alpha))
            surface.blit(blur_surface, (blur_rect.x - i, blur_rect.y - i))
    
    def draw_panel(self, surface: Surface, rect: pygame.Rect, 
                  background_color: Color = Colors.UI_BACKGROUND,
                  border_color: Color = Colors.FG_DARK,
                  animated: bool = True) -> None:
        """
        Desenha painel moderno com sombra e bordas arredondadas
        
        Args:
            surface: Superfície onde desenhar
            rect: Retângulo do painel
            background_color: Cor de fundo
            border_color: Cor da borda
            animated: Se deve aplicar animações
        """
        # Desenha sombra
        self._draw_shadow(surface, rect)
        
        # Animação sutil de respiração
        if animated:
            breath_factor = 1.0 + 0.02 * math.sin(self._animation_timer * 2)
            animated_rect = pygame.Rect(
                rect.x - int((rect.width * (breath_factor - 1)) / 2),
                rect.y - int((rect.height * (breath_factor - 1)) / 2),
                int(rect.width * breath_factor),
                int(rect.height * breath_factor)
            )
        else:
            animated_rect = rect
        
        # Cria painel com bordas arredondadas
        panel_surface = self._create_rounded_surface(
            (animated_rect.width, animated_rect.height),
            background_color,
            Effects.UI_CORNER_RADIUS,
            border_color,
            2
        )
        
        surface.blit(panel_surface, animated_rect.topleft)
    
    def draw_text_with_glow(self, surface: Surface, text: str, 
                           position: Tuple[int, int], font_size: str = 'medium',
                           text_color: Color = Colors.UI_PRIMARY,
                           glow_color: Optional[Color] = None,
                           glow_intensity: float = 0.5) -> pygame.Rect:
        """
        Desenha texto com efeito de brilho
        
        Args:
            surface: Superfície onde desenhar
            text: Texto a renderizar
            position: Posição central do texto
            font_size: Tamanho da fonte
            text_color: Cor do texto
            glow_color: Cor do brilho (usa text_color se None)
            glow_intensity: Intensidade do brilho
        """
        if glow_color is None:
            glow_color = text_color
        
        font = self.get_font(font_size)
        
        # Renderiza texto principal
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=position)
        
        # Efeito de brilho (múltiplas camadas)
        if glow_intensity > 0:
            for i in range(1, 4):
                glow_alpha = int(100 * glow_intensity / i)
                if glow_alpha > 0:
                    glow_surface = font.render(text, True, glow_color)
                    glow_surface.set_alpha(glow_alpha)
                    
                    # Desenha brilho em posições ligeiramente deslocadas
                    for dx in [-i, 0, i]:
                        for dy in [-i, 0, i]:
                            if dx != 0 or dy != 0:
                                glow_rect = text_rect.move(dx, dy)
                                surface.blit(glow_surface, glow_rect)
        
        # Desenha texto principal por cima
        surface.blit(text_surface, text_rect)
        
        return text_rect
    
    def draw_animated_hud(self, surface: Surface, score: int, length: int, 
                         level: int = 1, speed_multiplier: float = 1.0, 
                         food_stats: dict = None) -> None:
        """
        Desenha HUD moderno e animado
        
        Args:
            surface: Superfície onde desenhar
            score: Pontuação atual
            length: Tamanho da cobra
            level: Nível atual
            speed_multiplier: Multiplicador de velocidade
            food_stats: Estatísticas de comidas
        """
        # Painel principal do HUD (canto superior esquerdo)
        hud_width = 220
        hud_height = 140
        hud_rect = pygame.Rect(Effects.UI_PADDING, PLAY_AREA_HEIGHT + Effects.UI_PADDING, 
                              hud_width, hud_height)
        
        self.draw_panel(surface, hud_rect, Colors.UI_BACKGROUND, Colors.FG_DARK)
        
        # Conteúdo do painel
        y_offset = hud_rect.y + Effects.UI_PADDING + 5
        line_height = 25
        
        # Score com animação
        score_pulse = 1.0 + 0.1 * math.sin(self._animation_timer * 4)
        score_color = tuple(int(c * score_pulse) for c in Colors.UI_ACCENT)
        self.draw_text_with_glow(
            surface, f"Score: {score:,}", 
            (hud_rect.x + hud_width // 2, y_offset), 
            'medium', score_color, glow_intensity=0.3
        )
        y_offset += line_height
        
        # Tamanho da cobra
        self.draw_text_with_glow(
            surface, f"Length: {length}", 
            (hud_rect.x + hud_width // 2, y_offset), 
            'small', Colors.UI_PRIMARY
        )
        y_offset += line_height
        
        # Nível com destaque especial
        level_color = Colors.BRIGHT_YELLOW if level > 1 else Colors.UI_PRIMARY
        level_glow = 0.6 if level > 1 else 0.2
        self.draw_text_with_glow(
            surface, f"Level: {level}", 
            (hud_rect.x + hud_width // 2, y_offset), 
            'medium', level_color, glow_intensity=level_glow
        )
        y_offset += line_height
        
        # Velocidade com indicador visual
        speed_color = Colors.BRIGHT_RED if speed_multiplier > 2 else Colors.UI_SECONDARY
        self.draw_text_with_glow(
            surface, f"Speed: {speed_multiplier:.1f}x", 
            (hud_rect.x + hud_width // 2, y_offset), 
            'small', speed_color
        )
        
        # Painel de estatísticas de comidas (canto superior direito)
        if food_stats and any(food_stats.get(key, 0) > 0 for key in 
                             ['special_consumed', 'fugitive_consumed', 'mirror_consumed']):
            stats_width = 200
            stats_height = 100
            stats_rect = pygame.Rect(WINDOW_WIDTH - stats_width - Effects.UI_PADDING, 
                                   Effects.UI_PADDING, stats_width, stats_height)
            
            self.draw_panel(surface, stats_rect, Colors.UI_BACKGROUND, Colors.FG_DARK)
            
            stats_y = stats_rect.y + Effects.UI_PADDING
            stats_line_height = 20
            
            # Título
            self.draw_text_with_glow(
                surface, "Special Foods", 
                (stats_rect.centerx, stats_y + 10), 
                'small', Colors.UI_ACCENT, glow_intensity=0.2
            )
            stats_y += 25
            
            # Estatísticas com ícones coloridos
            if food_stats.get('special_consumed', 0) > 0:
                self.draw_text_with_glow(
                    surface, f"⭐ Gold: {food_stats['special_consumed']}", 
                    (stats_rect.centerx, stats_y), 
                    'small', Colors.FOOD_SPECIAL
                )
                stats_y += stats_line_height
            
            if food_stats.get('fugitive_consumed', 0) > 0:
                self.draw_text_with_glow(
                    surface, f"🏃‍♀️ Runner: {food_stats['fugitive_consumed']}", 
                    (stats_rect.centerx, stats_y), 
                    'small', Colors.FOOD_FUGITIVE
                )
                stats_y += stats_line_height
            
            if food_stats.get('mirror_consumed', 0) > 0:
                self.draw_text_with_glow(
                    surface, f"🪞 Mirror: {food_stats['mirror_consumed']}", 
                    (stats_rect.centerx, stats_y), 
                    'small', Colors.FOOD_MIRROR
                )

    def draw_hud(self, surface: Surface, score: int, length: int,
                 level: int = 1, speed_multiplier: float = 1.0,
                 food_stats: dict = None) -> None:
        """
        Compatibilidade retroativa: wrapper para draw_animated_hud.
        GameEngine e outros módulos chamam draw_hud(...), então
        mantemos essa assinatura e delegamos para a implementação
        atual (draw_animated_hud).
        """
        # delega para o método existente com a mesma assinatura
        return self.draw_animated_hud(
            surface=surface,
            score=score,
            length=length,
            level=level,
            speed_multiplier=speed_multiplier,
            food_stats=food_stats
        )

    def draw_level_up_notification(self, surface: Surface, level: int) -> None:
        """Desenha notificação animada de level up"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2 - 100
        
        # Painel animado com pulso
        pulse_factor = 1.0 + 0.3 * math.sin(self._animation_timer * 6)
        panel_width = int(400 * pulse_factor)
        panel_height = int(120 * pulse_factor)
        
        panel_rect = pygame.Rect(center_x - panel_width // 2, center_y - panel_height // 2,
                               panel_width, panel_height)
        
        # Cor baseada no nível
        bg_color_index = (level - 1) % len(Colors.RAINBOW_COLORS)
        bg_color = Colors.RAINBOW_COLORS[bg_color_index]
        
        # Painel com transparência
        panel_surface = self._create_rounded_surface(
            (panel_width, panel_height),
            (*bg_color, 200),
            Effects.UI_CORNER_RADIUS * 2
        )
        
        # Sombra dramática
        self._draw_shadow(surface, panel_rect, 200)
        
        surface.blit(panel_surface, panel_rect.topleft)
        
        # Texto "LEVEL UP!" com efeito dramático
        self.draw_text_with_glow(
            surface, Messages.LEVEL_UP,
            (center_x, center_y - 20),
            'extra_large', Colors.FG_LIGHT, 
            glow_intensity=0.8
        )
        
        # Número do nível
        level_text = f"Level {level}"
        self.draw_text_with_glow(
            surface, level_text,
            (center_x, center_y + 25),
            'large', Colors.FG_LIGHT,
            glow_intensity=0.5
        )
        
        # Partículas decorativas ao redor
        for i in range(8):
            angle = (self._animation_timer * 2 + i * math.pi / 4) % (2 * math.pi)
            radius = 80 + 20 * math.sin(self._animation_timer * 3 + i)
            
            particle_x = center_x + int(radius * math.cos(angle))
            particle_y = center_y + int(radius * math.sin(angle))
            
            particle_color = Colors.RAINBOW_COLORS[i % len(Colors.RAINBOW_COLORS)]
            particle_size = int(3 + 2 * math.sin(self._animation_timer * 4 + i))
            
            pygame.draw.circle(surface, particle_color, 
                             (particle_x, particle_y), particle_size)
    
    def draw_game_over_screen(self, surface: Surface, final_score: int) -> None:
        """Desenha tela de game over moderna"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Overlay escurecido
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.BG_DARK, 180))
        surface.blit(overlay, (0, 0))
        
        # Painel principal
        panel_width = 500
        panel_height = 300
        panel_rect = pygame.Rect(center_x - panel_width // 2, center_y - panel_height // 2,
                               panel_width, panel_height)
        
        self.draw_panel(surface, panel_rect, Colors.UI_BACKGROUND, Colors.RED)
        
        # Conteúdo
        y_pos = panel_rect.y + 40
        
        # Game Over
        self.draw_text_with_glow(
            surface, Messages.GAME_OVER,
            (center_x, y_pos),
            'extra_large', Colors.RED,
            glow_intensity=0.8
        )
        y_pos += 70
        
        # Score final
        score_text = Messages.FINAL_SCORE.format(score=final_score)
        self.draw_text_with_glow(
            surface, score_text,
            (center_x, y_pos),
            'large', Colors.UI_ACCENT,
            glow_intensity=0.4
        )
        y_pos += 50
        
        # Instruções piscantes
        blink_alpha = 0.7 + 0.3 * math.sin(self._animation_timer * 4)
        instruction_color = tuple(int(c * blink_alpha) for c in Colors.UI_SECONDARY)
        
        self.draw_text_with_glow(
            surface, Messages.RESTART_INSTRUCTION,
            (center_x, y_pos),
            'medium', instruction_color
        )
    
    def draw_pause_screen(self, surface: Surface) -> None:
        """Desenha tela de pausa moderna"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Overlay com blur simulado
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.BG_MEDIUM, 150))
        surface.blit(overlay, (0, 0))
        
        # Painel de pausa
        panel_width = 300
        panel_height = 120
        panel_rect = pygame.Rect(center_x - panel_width // 2, center_y - panel_height // 2,
                               panel_width, panel_height)
        
        self.draw_panel(surface, panel_rect, Colors.UI_BACKGROUND, Colors.UI_ACCENT)
        
        # Texto de pausa com animação
        pause_pulse = 1.0 + 0.2 * math.sin(self._animation_timer * 3)
        pause_color = tuple(int(c * pause_pulse) for c in Colors.UI_ACCENT)
        
        self.draw_text_with_glow(
            surface, Messages.PAUSED,
            (center_x, center_y),
            'large', pause_color,
            glow_intensity=0.6
        )
    
    def cleanup(self) -> None:
        """Limpa recursos da UI"""
        self._text_cache.clear()
        pygame.font.quit()
        print("🎨 ModernUIManager finalizado!")

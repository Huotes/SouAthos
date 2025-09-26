"""
Sistema de renderização avançado com tema Gruvbox
Substitui o renderer básico com gráficos modernos, gradientes e efeitos
Versão 3.0 com foco em qualidade visual e performance
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from utils.types import Surface, Color
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT, GRID_SIZE, 
    Colors, WINDOW_TITLE, Effects
)

class GradientHelper:
    """Utilitário para criar gradientes suaves otimizados"""
    
    @staticmethod
    def create_radial_gradient_fast(size: Tuple[int, int], center_color: Color, 
                                   edge_color: Color, radius_factor: float = 1.0) -> Surface:
        """
        Cria gradiente radial otimizado
        
        Args:
            size: Tamanho da superfície
            center_color: Cor do centro
            edge_color: Cor da borda
            radius_factor: Fator do raio (0.0-1.0)
        """
        surface = pygame.Surface(size, pygame.SRCALPHA)
        w, h = size
        center_x, center_y = w // 2, h // 2
        max_radius = int(min(w, h) // 2 * radius_factor)
        
        # Otimização: desenha círculos concêntricos ao invés de pixel por pixel
        steps = min(max_radius, 50)  # Limita passos para performance
        
        for i in range(steps, 0, -1):
            progress = 1.0 - (i / steps)
            current_radius = int(max_radius * (i / steps))
            
            # Interpola cores
            color = [
                int(center_color[j] * (1 - progress) + edge_color[j] * progress)
                for j in range(3)
            ]
            
            # Calcula alpha baseado na distância
            alpha = int(255 * (1 - progress * 0.3))
            
            # Desenha círculo
            if current_radius > 0:
                pygame.draw.circle(surface, (*color, alpha), 
                                 (center_x, center_y), current_radius)
        
        return surface
    
    @staticmethod
    def create_linear_gradient_fast(size: Tuple[int, int], start_color: Color, 
                                   end_color: Color, direction: str = 'vertical') -> Surface:
        """
        Cria gradiente linear otimizado
        
        Args:
            size: Tamanho da superfície
            start_color: Cor inicial
            end_color: Cor final
            direction: 'vertical' ou 'horizontal'
        """
        surface = pygame.Surface(size)
        w, h = size
        
        if direction == 'vertical':
            for y in range(h):
                progress = y / h
                color = [
                    int(start_color[i] * (1 - progress) + end_color[i] * progress)
                    for i in range(3)
                ]
                pygame.draw.line(surface, color, (0, y), (w, y))
        else:  # horizontal
            for x in range(w):
                progress = x / w
                color = [
                    int(start_color[i] * (1 - progress) + end_color[i] * progress)
                    for i in range(3)
                ]
                pygame.draw.line(surface, color, (x, 0), (x, h))
        
        return surface

class AmbientParticle:
    """Partícula ambiental otimizada para atmosfera Gruvbox"""
    
    def __init__(self):
        """Inicializa partícula com propriedades aleatórias"""
        self.x = random.uniform(-50, WINDOW_WIDTH + 50)
        self.y = random.uniform(-50, WINDOW_HEIGHT + 50)
        self.size = random.uniform(0.5, 2.5)
        self.speed = random.uniform(8, 25)
        self.direction = random.uniform(0, 2 * math.pi)
        self.base_alpha = random.randint(20, 60)
        self.alpha_variation = random.uniform(0.5, 1.5)
        
        # Cores Gruvbox para partículas
        self.color = random.choice([
            Colors.FG_DARK,
            Colors.BG_LIGHT, 
            Colors.YELLOW,
            Colors.ORANGE,
            Colors.AQUA
        ])
        
        self.lifetime = random.uniform(8, 20)
        self.age = 0
        self.drift_speed = random.uniform(0.5, 2.0)
        self.drift_offset = random.uniform(0, 2 * math.pi)
    
    def update(self, delta_time: float) -> None:
        """Atualiza posição e propriedades da partícula"""
        # Movimento principal
        self.x += math.cos(self.direction) * self.speed * delta_time
        self.y += math.sin(self.direction) * self.speed * delta_time
        
        # Drift sutil para movimento mais orgânico
        self.age += delta_time
        drift_x = math.sin(self.age * self.drift_speed + self.drift_offset) * 2
        drift_y = math.cos(self.age * self.drift_speed * 1.3 + self.drift_offset) * 1.5
        
        self.x += drift_x * delta_time
        self.y += drift_y * delta_time
        
        # Wrap around com margem
        margin = 100
        if self.x < -margin:
            self.x = WINDOW_WIDTH + margin
        elif self.x > WINDOW_WIDTH + margin:
            self.x = -margin
        
        if self.y < -margin:
            self.y = WINDOW_HEIGHT + margin
        elif self.y > WINDOW_HEIGHT + margin:
            self.y = -margin
    
    def draw(self, surface: Surface) -> None:
        """Desenha partícula com brilho suave otimizado"""
        # Calcula alpha dinâmico
        life_factor = min(self.age / 2, (self.lifetime - self.age) / 3, 1)
        breath_factor = 1 + 0.3 * math.sin(self.age * self.alpha_variation)
        current_alpha = int(self.base_alpha * life_factor * breath_factor)
        
        if current_alpha <= 5:
            return
        
        # Tamanho dinâmico
        current_size = max(0.5, self.size * life_factor)
        
        # Otimização: apenas uma camada de brilho para partículas pequenas
        if current_size < 1.5:
            # Partícula simples
            pygame.draw.circle(surface, self.color, 
                             (int(self.x), int(self.y)), int(current_size))
        else:
            # Partícula com brilho sutil
            glow_surface = pygame.Surface((int(current_size * 4), int(current_size * 4)), pygame.SRCALPHA)
            glow_center = (int(current_size * 2), int(current_size * 2))
            
            # Brilho externo
            pygame.draw.circle(glow_surface, (*self.color, current_alpha // 3), 
                             glow_center, int(current_size * 1.5))
            
            # Núcleo principal
            pygame.draw.circle(glow_surface, (*self.color, current_alpha), 
                             glow_center, int(current_size))
            
            surface.blit(glow_surface, 
                        (int(self.x - current_size * 2), int(self.y - current_size * 2)))
    
    def is_alive(self) -> bool:
        """Verifica se a partícula ainda está viva"""
        return self.age < self.lifetime

class Renderer:
    """
    Sistema de renderização avançado com tema Gruvbox v3.0
    
    Recursos implementados:
    - Fundo com gradiente animado
    - Grid transparente moderno
    - Partículas ambientais otimizadas  
    - Sombras realistas
    - Efeitos de pós-processamento
    - Sistema de cache para performance
    """
    
    def __init__(self):
        """Inicializa o renderer avançado"""
        pygame.display.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Superfícies cachadas para performance
        self._background_cache = self._create_dynamic_background()
        self._grid_cache = self._create_grid_cache()
        
        # Superfícies de trabalho
        self._shadow_layer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self._effect_layer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Estados dos efeitos especiais
        self._level_up_timer = 0.0
        self._level_up_active = False
        self._mirror_effect_timer = 0.0
        self._mirror_effect_active = False
        self._screen_flash_timer = 0.0
        self._screen_flash_active = False
        self._flash_color = Colors.BRIGHT_YELLOW
        
        # Sistema de partículas ambientais
        self._ambient_particles: List[AmbientParticle] = []
        self._particle_spawn_timer = 0.0
        self._initialize_particles()
        
        # Timer global para animações
        self._animation_timer = 0.0
        self._background_shift = 0.0
        
        print("🎨 Renderer v3.0 Gruvbox inicializado!")
        print("✨ Gradientes, partículas e sombras ativados!")
    
    def _create_dynamic_background(self) -> Surface:
        """Cria fundo dinâmico com gradiente Gruvbox"""
        return GradientHelper.create_radial_gradient_fast(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            Colors.BG_MEDIUM,    # Centro mais claro
            Colors.BG_DARK,      # Bordas mais escuras
            0.9
        )
    
    def _create_grid_cache(self) -> Surface:
        """Cria cache do grid para melhor performance"""
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Grid sutil com tema Gruvbox
        grid_color = (*Colors.GRID_COLOR, Effects.GRID_TRANSPARENCY)
        
        # Linhas verticais
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(grid_surface, grid_color, (x, 0), (x, WINDOW_HEIGHT), 1)
        
        # Linhas horizontais
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid_surface, grid_color, (0, y), (WINDOW_WIDTH, y), 1)
        
        return grid_surface
    
    def _initialize_particles(self) -> None:
        """Inicializa sistema de partículas ambientais"""
        particle_count = Effects.AMBIENT_PARTICLE_COUNT
        for _ in range(particle_count):
            self._ambient_particles.append(AmbientParticle())
    
    @property
    def screen(self) -> Surface:
        """Retorna a superfície da tela principal"""
        return self._screen
    
    def clear_screen(self, animated: bool = True) -> None:
        """
        Limpa a tela com fundo dinâmico Gruvbox
        
        Args:
            animated: Se deve usar animação de fundo
        """
        if animated:
            self._screen.fill(Colors.BG_DARK)

            # retângulo da área jogável
            play_area_rect = pygame.Rect(0, 0, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)

            # preencher fundo do campo
            pygame.draw.rect(self._screen, Colors.BG_DARK, play_area_rect)

            # desenhar bordas
            pygame.draw.rect(self._screen, Colors.UI_ACCENT, play_area_rect, width=4)
    
    def draw_grid(self, animated: bool = True) -> None:
        """
        Desenha grid moderno com efeitos Gruvbox
        
        Args:
            animated: Se deve aplicar efeitos de level up
        """
        if self._level_up_active and animated:
            # Grid colorido para level up
            color_index = int((self._level_up_timer * 6) % len(Colors.RAINBOW_COLORS))
            rainbow_color = Colors.RAINBOW_COLORS[color_index]
            
            # Intensidade pulsante
            intensity = 0.8 + 0.2 * abs(math.sin(self._level_up_timer * 8))
            animated_color = tuple(int(c * intensity) for c in rainbow_color)
            
            # Cria grid temporário animado
            temp_grid = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            
            alpha = int(120 * intensity)
            
            # Linhas com efeito de brilho
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                pygame.draw.line(temp_grid, (*animated_color, alpha), 
                               (x, 0), (x, WINDOW_HEIGHT), 2)
            
            for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
                pygame.draw.line(temp_grid, (*animated_color, alpha),
                               (0, y), (WINDOW_WIDTH, y), 2)
            
            self._screen.blit(temp_grid, (0, 0), special_flags=pygame.BLEND_ADD)
        else:
            # Grid normal cached
            self._screen.blit(self._grid_cache, (0, 0))
    
    def update_ambient_particles(self, delta_time: float) -> None:
        """Atualiza sistema de partículas ambientais"""
        # Atualiza partículas existentes
        for particle in self._ambient_particles[:]:
            particle.update(delta_time)
            if not particle.is_alive():
                self._ambient_particles.remove(particle)
        
        # Spawna novas partículas conforme necessário
        self._particle_spawn_timer += delta_time
        spawn_interval = 0.5  # Uma nova partícula a cada 0.5s
        
        if self._particle_spawn_timer >= spawn_interval:
            self._particle_spawn_timer = 0.0
            if len(self._ambient_particles) < Effects.AMBIENT_PARTICLE_COUNT:
                self._ambient_particles.append(AmbientParticle())
    
    def draw_ambient_particles(self) -> None:
        """Desenha partículas ambientais otimizado"""
        for particle in self._ambient_particles:
            particle.draw(self._screen)
    
    def draw_shadow(self, center: Tuple[int, int], radius: int, 
                   intensity: int = Effects.SHADOW_ALPHA) -> None:
        """
        Desenha sombra circular suave otimizada
        
        Args:
            center: Centro da sombra
            radius: Raio da sombra
            intensity: Intensidade (0-255)
        """
        if intensity <= 0:
            return
        
        shadow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        shadow_center = (radius * 2, radius * 2)
        
        # Sombra com gradiente radial simples
        for i in range(3, 0, -1):
            shadow_radius = radius + i * 2
            shadow_alpha = intensity // (i + 1)
            
            if shadow_alpha > 0:
                pygame.draw.circle(shadow_surface, (*Colors.SHADOW_COLOR, shadow_alpha),
                                 shadow_center, shadow_radius)
        
        # Posição da sombra com deslocamento
        shadow_x = center[0] - radius * 2 + Effects.SHADOW_OFFSET
        shadow_y = center[1] - radius * 2 + Effects.SHADOW_OFFSET
        
        self._screen.blit(shadow_surface, (shadow_x, shadow_y), 
                         special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def draw_glow_circle(self, center: Tuple[int, int], radius: int, 
                        color: Color, intensity: float = 1.0) -> None:
        """
        Desenha círculo com brilho Gruvbox otimizado
        
        Args:
            center: Centro do círculo
            radius: Raio base
            color: Cor principal
            intensity: Intensidade do brilho (0.0-1.0)
        """
        if intensity <= 0:
            return
        
        glow_surface = pygame.Surface((radius * 6, radius * 6), pygame.SRCALPHA)
        glow_center = (radius * 3, radius * 3)
        
        # Múltiplas camadas de brilho
        for i in range(4, 0, -1):
            glow_radius = int(radius + i * 4 * intensity)
            alpha = int(60 * intensity / i)
            
            if alpha > 5:
                pygame.draw.circle(glow_surface, (*color, alpha),
                                 glow_center, glow_radius)
        
        # Círculo principal
        pygame.draw.circle(glow_surface, color, glow_center, radius)
        
        # Posiciona na tela
        glow_x = center[0] - radius * 3
        glow_y = center[1] - radius * 3
        
        self._screen.blit(glow_surface, (glow_x, glow_y), 
                         special_flags=pygame.BLEND_ADD)
    
    def update_effects(self, delta_time: float) -> None:
        """
        Atualiza todos os efeitos visuais
        
        Args:
            delta_time: Tempo decorrido desde última atualização
        """
        self._animation_timer += delta_time
        
        # Efeito de level up
        if self._level_up_active:
            self._level_up_timer += delta_time
            if self._level_up_timer >= Effects.LEVEL_UP_FLASH_DURATION:
                self._level_up_active = False
                self._level_up_timer = 0.0
                print("🌈 Efeito de level up finalizado")
        
        # Efeito espelho
        if self._mirror_effect_active:
            self._mirror_effect_timer += delta_time
            if self._mirror_effect_timer >= Effects.MIRROR_EFFECT_DURATION:
                self._mirror_effect_active = False
                self._mirror_effect_timer = 0.0
                print("🪞 Efeito de espelho finalizado")
        
        # Flash da tela
        if self._screen_flash_active:
            self._screen_flash_timer += delta_time
            if self._screen_flash_timer >= Effects.SPECIAL_CONSUME_EFFECT_DURATION:
                self._screen_flash_active = False
                self._screen_flash_timer = 0.0
                print("⚡ Flash da tela finalizado")
        
        # Partículas ambientais
        self.update_ambient_particles(delta_time)
    
    def start_level_up_effect(self) -> None:
        """Inicia efeito visual de level up"""
        self._level_up_active = True
        self._level_up_timer = 0.0
        print("🌈 Efeito de level up Gruvbox ativado!")
    
    def start_mirror_effect(self) -> None:
        """Inicia efeito visual de espelho"""
        self._mirror_effect_active = True
        self._mirror_effect_timer = 0.0
        print("🪞 Efeito de espelho Gruvbox ativado!")
    
    def start_screen_flash(self, color: Color = Colors.BRIGHT_YELLOW) -> None:
        """
        Inicia efeito de flash na tela
        
        Args:
            color: Cor do flash
        """
        self._screen_flash_active = True
        self._screen_flash_timer = 0.0
        self._flash_color = color
        print(f"⚡ Flash Gruvbox ativado: {color}!")
    
    def apply_mirror_transform(self, surface: Surface) -> None:
        """
        Aplica transformação de espelhamento suave
        
        Args:
            surface: Superfície a ser espelhada
        """
        if not self._mirror_effect_active:
            return
        
        # Cria superfície espelhada
        flipped_surface = pygame.transform.flip(surface, True, False)
        
        # Calcula intensidade do efeito
        progress = self._mirror_effect_timer / Effects.MIRROR_EFFECT_DURATION
        alpha = int(200 * (1.0 - progress))  # Desvanece gradualmente
        
        if alpha > 10:
            flipped_surface.set_alpha(alpha)
            surface.blit(flipped_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def apply_screen_flash(self, surface: Surface) -> None:
        """
        Aplica efeito de flash com gradiente Gruvbox
        
        Args:
            surface: Superfície onde aplicar o flash
        """
        if not self._screen_flash_active:
            return
        
        progress = self._screen_flash_timer / Effects.SPECIAL_CONSUME_EFFECT_DURATION
        intensity = Effects.SCREEN_FLASH_INTENSITY * (1.0 - progress)
        
        if intensity > 5:
            # Flash com gradiente radial
            flash_surface = GradientHelper.create_radial_gradient_fast(
                (WINDOW_WIDTH, WINDOW_HEIGHT),
                self._flash_color,
                Colors.BG_DARK,
                0.7
            )
            flash_surface.set_alpha(int(intensity))
            surface.blit(flash_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def present(self) -> None:
        """Apresenta o frame final com todos os efeitos"""
        # Desenha partículas ambientais (camada de fundo)
        self.draw_ambient_particles()
        
        # Aplica efeitos de pós-processamento
        if self._mirror_effect_active:
            self.apply_mirror_transform(self._screen)
        
        if self._screen_flash_active:
            self.apply_screen_flash(self._screen)
        
        # Atualiza display
        pygame.display.flip()
    
    def cleanup(self) -> None:
        """Limpa recursos do renderer"""
        self._ambient_particles.clear()
        pygame.display.quit()
        print("🎨 Renderer v3.0 finalizado!")
    
    # Properties para compatibilidade com código existente
    def is_level_up_active(self) -> bool:
        """Verifica se efeito de level up está ativo"""
        return self._level_up_active
    
    def is_mirror_effect_active(self) -> bool:
        """Verifica se efeito de espelho está ativo"""
        return self._mirror_effect_active
    
    def get_animation_time(self) -> float:
        """Retorna tempo atual das animações"""
        return self._animation_timer

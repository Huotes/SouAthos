"""
Classes de comida refatoradas com tipos especiais
Inclui: Comida Normal, Especial (5 pontos) e Fugitiva (com rastro)
Princípios POO: Herança, polimorfismo, responsabilidade única
"""

import pygame
import random
import math
from typing import List, Tuple, Optional
from utils.types import Position, Surface, SnakeBody
from entities.game_object import GameObject
from utils.enums import EntityType
from config.settings import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, Colors,
    SPECIAL_FOOD_POINTS, FUGITIVE_FOOD_POINTS, POINTS_PER_FOOD,
    FUGITIVE_FOOD_BLINK_SPEED, FUGITIVE_FOOD_TRAIL_DURATION
)

class Food(GameObject):
    """
    Classe base para comida do jogo
    
    Responsabilidades:
    - Geração de posições aleatórias
    - Evitar spawnar no corpo da cobra
    - Sistema base de renderização
    - Detecção de colisão com a cobra
    """
    
    def __init__(self, food_type: EntityType = EntityType.FOOD_NORMAL):
        """
        Inicializa a comida
        
        Args:
            food_type: Tipo da comida (normal, especial, fugitiva)
        """
        initial_position = self._generate_random_position()
        super().__init__(initial_position, food_type)
        self._animation_counter = 0.0
        self._points_value = POINTS_PER_FOOD
    
    @property
    def points_value(self) -> int:
        """Retorna o valor em pontos desta comida"""
        return self._points_value
    
    def _generate_random_position(self) -> Position:
        """
        Gera uma posição aleatória no grid
        
        Returns:
            Nova posição (x, y)
        """
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def respawn(self, snake_body: SnakeBody, max_attempts: int = 100) -> None:
        """
        Reposiciona a comida evitando o corpo da cobra
        
        Args:
            snake_body: Lista com posições do corpo da cobra
            max_attempts: Máximo de tentativas para encontrar posição válida
        """
        for _ in range(max_attempts):
            new_position = self._generate_random_position()
            if new_position not in snake_body:
                self._position = new_position
                self._animation_counter = 0.0
                return
        
        # Fallback: encontra qualquer posição livre (força bruta)
        all_positions = {(x, y) for x in range(GRID_WIDTH) 
                        for y in range(GRID_HEIGHT)}
        available_positions = all_positions - set(snake_body)
        
        if available_positions:
            self._position = random.choice(list(available_positions))
            self._animation_counter = 0.0
    
    def update_animation(self, delta_time: float = 1.0) -> None:
        """
        Atualiza a animação da comida
        
        Args:
            delta_time: Tempo decorrido desde a última atualização
        """
        self._animation_counter += delta_time * 0.2
    
    def draw(self, surface: Surface) -> None:
        """
        Desenha a comida normal
        
        Args:
            surface: Superfície onde desenhar
        """
        if not self.active:
            return
        
        x, y = self.position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Efeito pulsante sutil
        pulse_factor = 1.0 + 0.05 * math.sin(self._animation_counter)
        radius = int((GRID_SIZE // 2 - 1) * pulse_factor)
        
        # Desenha círculo vermelho
        pygame.draw.circle(surface, Colors.RED, (center_x, center_y), radius)
        pygame.draw.circle(surface, (200, 0, 0), (center_x, center_y), radius - 2)
        
        # Brilho no centro
        highlight_radius = max(2, radius // 3)
        highlight_x = center_x - radius // 3
        highlight_y = center_y - radius // 3
        pygame.draw.circle(surface, (255, 100, 100), 
                         (highlight_x, highlight_y), highlight_radius)
        
        # Borda
        pygame.draw.circle(surface, Colors.BLACK, (center_x, center_y), radius, 1)
    
    def get_bounds(self) -> pygame.Rect:
        """
        Retorna os limites da comida para detecção de colisão
        
        Returns:
            Retângulo da comida
        """
        x, y = self.position
        return pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    
    def consume(self) -> int:
        """
        Consome a comida (desativa e retorna pontos)
        
        Returns:
            Pontos obtidos pela comida
        """
        self.deactivate()
        return self._points_value

class SpecialFood(Food):
    """
    Comida especial com 5 pontos e visual dourado com contorno
    """
    
    def __init__(self):
        """Inicializa comida especial"""
        super().__init__(EntityType.FOOD_SPECIAL)
        self._points_value = SPECIAL_FOOD_POINTS
        self._border_animation = 0.0
    
    def update_animation(self, delta_time: float = 1.0) -> None:
        """Atualiza animação da comida especial"""
        super().update_animation(delta_time)
        self._border_animation += delta_time * 2.0  # Animação mais rápida para o contorno
    
    def draw(self, surface: Surface) -> None:
        """Desenha comida especial com contorno animado"""
        if not self.active:
            return
        
        x, y = self.position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Efeito pulsante mais intenso
        pulse_factor = 1.0 + 0.15 * math.sin(self._animation_counter * 1.5)
        radius = int((GRID_SIZE // 2 - 1) * pulse_factor)
        
        # Contorno animado (borda externa)
        border_pulse = 1.0 + 0.3 * math.sin(self._border_animation)
        border_radius = int(radius * border_pulse) + 3
        
        # Desenha contorno dourado animado
        for i in range(3):
            border_alpha = int(255 * (1.0 - i * 0.3))
            border_color = (*Colors.SPECIAL_FOOD_BORDER, border_alpha)
            
            # Cria superfície com alpha para o contorno
            border_surface = pygame.Surface((border_radius * 2 + 4, border_radius * 2 + 4))
            border_surface.set_alpha(border_alpha)
            border_surface.set_colorkey(Colors.BLACK)
            
            pygame.draw.circle(border_surface, Colors.SPECIAL_FOOD_BORDER, 
                             (border_radius + 2, border_radius + 2), border_radius - i, 2)
            
            surface.blit(border_surface, 
                        (center_x - border_radius - 2, center_y - border_radius - 2))
        
        # Desenha comida principal dourada
        pygame.draw.circle(surface, Colors.SPECIAL_FOOD_COLOR, (center_x, center_y), radius)
        pygame.draw.circle(surface, (200, 180, 0), (center_x, center_y), radius - 2)
        
        # Estrela no centro (indicador de especial)
        star_radius = radius // 2
        if star_radius >= 3:
            star_points = []
            for i in range(8):  # 8 pontos para uma estrela
                angle = i * math.pi / 4
                if i % 2 == 0:  # Pontos externos
                    px = center_x + int(star_radius * math.cos(angle))
                    py = center_y + int(star_radius * math.sin(angle))
                else:  # Pontos internos
                    px = center_x + int(star_radius * 0.4 * math.cos(angle))
                    py = center_y + int(star_radius * 0.4 * math.sin(angle))
                star_points.append((px, py))
            
            if len(star_points) >= 6:
                pygame.draw.polygon(surface, Colors.WHITE, star_points)
        
        # Borda principal
        pygame.draw.circle(surface, Colors.BLACK, (center_x, center_y), radius, 2)

class TrailParticle:
    """
    Partícula de rastro para comida fugitiva
    """
    
    def __init__(self, position: Position, duration: float = FUGITIVE_FOOD_TRAIL_DURATION):
        """
        Inicializa partícula de rastro
        
        Args:
            position: Posição da partícula
            duration: Duração em segundos
        """
        self.position = position
        self.max_duration = duration
        self.remaining_time = duration
        self.active = True
    
    def update(self, delta_time: float) -> None:
        """
        Atualiza a partícula
        
        Args:
            delta_time: Tempo decorrido
        """
        self.remaining_time -= delta_time
        if self.remaining_time <= 0:
            self.active = False
    
    def draw(self, surface: Surface) -> None:
        """
        Desenha a partícula de rastro
        
        Args:
            surface: Superfície onde desenhar
        """
        if not self.active:
            return
        
        x, y = self.position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Calcula alpha baseado no tempo restante
        alpha_factor = self.remaining_time / self.max_duration
        alpha = int(100 * alpha_factor)  # Alpha de 0 a 100
        
        # Tamanho da partícula diminui com o tempo
        radius = int((GRID_SIZE // 4) * alpha_factor) + 1
        
        # Cria superfície com alpha
        particle_surface = pygame.Surface((radius * 2 + 2, radius * 2 + 2))
        particle_surface.set_alpha(alpha)
        particle_surface.set_colorkey(Colors.BLACK)
        
        # Desenha círculo violeta
        pygame.draw.circle(particle_surface, Colors.FUGITIVE_FOOD_COLOR, 
                         (radius + 1, radius + 1), radius)
        
        surface.blit(particle_surface, 
                    (center_x - radius - 1, center_y - radius - 1))

class FugitiveFood(Food):
    """
    Comida fugitiva que pisca e foge quando a cobra se aproxima
    """
    
    def __init__(self):
        """Inicializa comida fugitiva"""
        super().__init__(EntityType.FOOD_FUGITIVE)
        self._points_value = FUGITIVE_FOOD_POINTS
        self._blink_timer = 0.0
        self._trail_particles: List[TrailParticle] = []
        self._escape_cooldown = 0.0  # Cooldown entre fugas
    
    def update_animation(self, delta_time: float = 1.0) -> None:
        """Atualiza animação da comida fugitiva"""
        super().update_animation(delta_time)
        self._blink_timer += delta_time * FUGITIVE_FOOD_BLINK_SPEED
        
        # Atualiza cooldown de fuga
        if self._escape_cooldown > 0:
            self._escape_cooldown -= delta_time
        
        # Atualiza partículas de rastro
        for particle in self._trail_particles[:]:  # Cópia da lista
            particle.update(delta_time)
            if not particle.active:
                self._trail_particles.remove(particle)
    
    def _is_snake_nearby(self, snake_body: SnakeBody, danger_radius: int = 2) -> bool:
        """
        Verifica se a cobra está próxima
        
        Args:
            snake_body: Corpo da cobra
            danger_radius: Raio de perigo em células
            
        Returns:
            True se cobra estiver próxima
        """
        food_x, food_y = self.position
        
        for segment_x, segment_y in snake_body:
            distance = abs(segment_x - food_x) + abs(segment_y - food_y)  # Distância Manhattan
            if distance <= danger_radius:
                return True
        
        return False
    
    def try_escape(self, snake_body: SnakeBody) -> bool:
        """
        Tenta fugir da cobra se ela estiver próxima
        
        Args:
            snake_body: Corpo da cobra
            
        Returns:
            True se fugiu, False caso contrário
        """
        # Verifica cooldown e proximidade
        if self._escape_cooldown > 0 or not self._is_snake_nearby(snake_body):
            return False
        
        # Adiciona partícula de rastro na posição atual
        self._trail_particles.append(TrailParticle(self.position))
        
        # Encontra nova posição longe da cobra
        old_position = self.position
        best_position = None
        max_distance = 0
        
        # Tenta várias posições e escolhe a mais longe da cobra
        for _ in range(50):  # 50 tentativas
            candidate = self._generate_random_position()
            if candidate in snake_body:
                continue
            
            # Calcula distância mínima da cobra
            min_distance = min(
                abs(candidate[0] - seg[0]) + abs(candidate[1] - seg[1])
                for seg in snake_body
            )
            
            if min_distance > max_distance:
                max_distance = min_distance
                best_position = candidate
        
        # Move para nova posição se encontrou uma boa
        if best_position and max_distance >= 3:
            self._position = best_position
            self._escape_cooldown = 1.0  # 1 segundo de cooldown
            print(f"🏃‍♀️ Comida fugitiva escapou de {old_position} para {best_position}!")
            return True
        
        return False
    
    def draw(self, surface: Surface) -> None:
        """Desenha comida fugitiva com efeito piscante"""
        if not self.active:
            return
        
        # Desenha rastro primeiro (atrás da comida)
        for particle in self._trail_particles:
            particle.draw(surface)
        
        # Efeito piscante
        blink_factor = math.sin(self._blink_timer)
        if blink_factor < -0.3:  # Fica invisível parte do tempo
            return
        
        x, y = self.position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Efeito pulsante baseado no piscar
        pulse_factor = 1.0 + 0.2 * abs(blink_factor)
        radius = int((GRID_SIZE // 2 - 1) * pulse_factor)
        
        # Intensidade da cor baseada no piscar
        color_intensity = 0.7 + 0.3 * abs(blink_factor)
        fugitive_color = tuple(int(c * color_intensity) for c in Colors.FUGITIVE_FOOD_COLOR)
        
        # Desenha comida principal (violeta)
        pygame.draw.circle(surface, fugitive_color, (center_x, center_y), radius)
        
        # Efeito de "energia" ao redor
        if blink_factor > 0.5:  # Quando está mais visível
            energy_radius = radius + 3
            energy_alpha = int(100 * (blink_factor - 0.5) * 2)
            
            energy_surface = pygame.Surface((energy_radius * 2 + 2, energy_radius * 2 + 2))
            energy_surface.set_alpha(energy_alpha)
            energy_surface.set_colorkey(Colors.BLACK)
            
            pygame.draw.circle(energy_surface, Colors.FUGITIVE_FOOD_COLOR,
                             (energy_radius + 1, energy_radius + 1), energy_radius, 2)
            
            surface.blit(energy_surface, 
                        (center_x - energy_radius - 1, center_y - energy_radius - 1))
        
        # Símbolo de raio no centro (indicador de fugitiva)
        if radius >= 6:
            lightning_points = [
                (center_x - radius//3, center_y - radius//2),
                (center_x + radius//6, center_y - radius//4),
                (center_x - radius//6, center_y),
                (center_x + radius//3, center_y + radius//2),
                (center_x - radius//6, center_y + radius//4),
                (center_x + radius//6, center_y),
            ]
            
            if len(lightning_points) >= 3:
                pygame.draw.polygon(surface, Colors.WHITE, lightning_points)
        
        # Borda principal
        pygame.draw.circle(surface, Colors.BLACK, (center_x, center_y), radius, 1)

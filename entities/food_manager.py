"""
Gerenciador de comidas especiais
Controla spawn, tipos e interações das diferentes comidas
Princípio de responsabilidade única: Apenas gerenciamento de comidas
"""

import random
from typing import Optional, Union
from utils.types import SnakeBody
from entities.food import Food, SpecialFood, FugitiveFood
from utils.enums import EntityType
from config.settings import (
    SPECIAL_FOOD_SPAWN_CHANCE, 
    FUGITIVE_FOOD_SPAWN_CHANCE
)

class FoodManager:
    """
    Gerenciador centralizado das comidas do jogo
    
    Responsabilidades:
    - Controlar spawning de diferentes tipos
    - Gerenciar comida ativa
    - Coordenar interações especiais
    - Estatísticas de comidas consumidas
    """
    
    def __init__(self):
        """Inicializa o gerenciador de comidas"""
        self._current_food: Optional[Union[Food, SpecialFood, FugitiveFood]] = None
        self._spawn_normal_food()
        
        # Estatísticas
        self._stats = {
            'normal_consumed': 0,
            'special_consumed': 0,
            'fugitive_consumed': 0,
            'fugitive_escapes': 0
        }
    
    @property
    def current_food(self) -> Optional[Union[Food, SpecialFood, FugitiveFood]]:
        """Retorna a comida atual"""
        return self._current_food
    
    @property
    def stats(self) -> dict:
        """Retorna estatísticas de consumo"""
        return self._stats.copy()
    
    def _spawn_normal_food(self) -> None:
        """Spawna comida normal"""
        self._current_food = Food(EntityType.FOOD_NORMAL)
        print("🍎 Comida normal spawnada")
    
    def _spawn_special_food(self) -> None:
        """Spawna comida especial (5 pontos)"""
        self._current_food = SpecialFood()
        print("⭐ Comida ESPECIAL spawnada! (+5 pontos)")
    
    def _spawn_fugitive_food(self) -> None:
        """Spawna comida fugitiva"""
        self._current_food = FugitiveFood()
        print("🏃‍♀️ Comida FUGITIVA spawnada! (tente pegá-la!)")
    
    def _determine_food_type(self) -> EntityType:
        """
        Determina que tipo de comida spawnar baseado nas chances
        
        Returns:
            Tipo de comida a ser spawnada
        """
        rand_value = random.random()
        
        # Ordem de prioridade: Fugitiva > Especial > Normal
        if rand_value < FUGITIVE_FOOD_SPAWN_CHANCE:
            return EntityType.FOOD_FUGITIVE
        elif rand_value < FUGITIVE_FOOD_SPAWN_CHANCE + SPECIAL_FOOD_SPAWN_CHANCE:
            return EntityType.FOOD_SPECIAL
        else:
            return EntityType.FOOD_NORMAL
    
    def spawn_new_food(self, snake_body: SnakeBody) -> None:
        """
        Spawna nova comida evitando o corpo da cobra
        
        Args:
            snake_body: Corpo da cobra para evitar
        """
        food_type = self._determine_food_type()
        
        # Cria comida baseada no tipo
        if food_type == EntityType.FOOD_SPECIAL:
            self._spawn_special_food()
        elif food_type == EntityType.FOOD_FUGITIVE:
            self._spawn_fugitive_food()
        else:
            self._spawn_normal_food()
        
        # Reposiciona evitando a cobra
        if self._current_food:
            self._current_food.respawn(snake_body)
    
    def update(self, delta_time: float, snake_body: SnakeBody) -> None:
        """
        Atualiza a comida atual
        
        Args:
            delta_time: Tempo decorrido
            snake_body: Corpo da cobra
        """
        if not self._current_food or not self._current_food.active:
            return
        
        # Atualiza animação
        self._current_food.update_animation(delta_time)
        
        # Lógica especial para comida fugitiva
        if isinstance(self._current_food, FugitiveFood):
            # Tenta fugir se cobra estiver próxima
            if self._current_food.try_escape(snake_body):
                self._stats['fugitive_escapes'] += 1
    
    def consume_current_food(self) -> int:
        """
        Consome a comida atual
        
        Returns:
            Pontos obtidos pela comida
        """
        if not self._current_food or not self._current_food.active:
            return 0
        
        points = self._current_food.consume()
        
        # Atualiza estatísticas
        if self._current_food.entity_type == EntityType.FOOD_NORMAL:
            self._stats['normal_consumed'] += 1
            print(f"🍎 Comida normal consumida! (+{points} pontos)")
        elif self._current_food.entity_type == EntityType.FOOD_SPECIAL:
            self._stats['special_consumed'] += 1
            print(f"⭐ Comida ESPECIAL consumida! (+{points} pontos)")
        elif self._current_food.entity_type == EntityType.FOOD_FUGITIVE:
            self._stats['fugitive_consumed'] += 1
            print(f"🏃‍♀️ Comida FUGITIVA capturada! (+{points} pontos)")
        
        return points
    
    def draw(self, surface) -> None:
        """
        Desenha a comida atual
        
        Args:
            surface: Superfície onde desenhar
        """
        if self._current_food and self._current_food.active:
            self._current_food.draw(surface)
    
    def get_bounds(self) -> Optional:
        """
        Retorna os limites da comida atual
        
        Returns:
            Retângulo da comida ou None
        """
        if self._current_food and self._current_food.active:
            return self._current_food.get_bounds()
        return None
    
    def get_position(self) -> Optional:
        """
        Retorna a posição da comida atual
        
        Returns:
            Posição da comida ou None
        """
        if self._current_food and self._current_food.active:
            return self._current_food.position
        return None
    
    def check_collision(self, other_bounds) -> bool:
        """
        Verifica colisão da comida atual com outro objeto
        
        Args:
            other_bounds: Limites do outro objeto
            
        Returns:
            True se houver colisão
        """
        if not self._current_food or not self._current_food.active:
            return False
        
        food_bounds = self._current_food.get_bounds()
        return food_bounds.colliderect(other_bounds) if food_bounds else False
    
    def is_food_active(self) -> bool:
        """
        Verifica se há comida ativa
        
        Returns:
            True se há comida ativa
        """
        return self._current_food is not None and self._current_food.active
    
    def get_food_type(self) -> Optional[EntityType]:
        """
        Retorna o tipo da comida atual
        
        Returns:
            Tipo da comida atual ou None
        """
        if self._current_food:
            return self._current_food.entity_type
        return None
    
    def print_statistics(self) -> None:
        """Imprime estatísticas de consumo de comidas"""
        total_consumed = sum([
            self._stats['normal_consumed'],
            self._stats['special_consumed'], 
            self._stats['fugitive_consumed']
        ])
        
        print("\n📊 === ESTATÍSTICAS DE COMIDAS ===")
        print(f"🍎 Normais consumidas: {self._stats['normal_consumed']}")
        print(f"⭐ Especiais consumidas: {self._stats['special_consumed']}")
        print(f"🏃‍♀️ Fugitivas capturadas: {self._stats['fugitive_consumed']}")
        print(f"💨 Fugas bem-sucedidas: {self._stats['fugitive_escapes']}")
        print(f"🎯 Total de comidas: {total_consumed}")
        
        if total_consumed > 0:
            special_rate = (self._stats['special_consumed'] / total_consumed) * 100
            fugitive_rate = (self._stats['fugitive_consumed'] / total_consumed) * 100
            print(f"⭐ Taxa de especiais: {special_rate:.1f}%")
            print(f"🏃‍♀️ Taxa de fugitivas: {fugitive_rate:.1f}%")
        
        print("=" * 35)
    
    def reset(self) -> None:
        """Reseta o gerenciador para estado inicial"""
        # Reseta comida atual
        if self._current_food:
            self._current_food.deactivate()
        
        # Spawna nova comida normal
        self._spawn_normal_food()
        
        # Limpa estatísticas
        self._stats = {
            'normal_consumed': 0,
            'special_consumed': 0,
            'fugitive_consumed': 0,
            'fugitive_escapes': 0
        }
        
        print("🔄 Gerenciador de comidas resetado")
    
    def force_spawn_type(self, food_type: EntityType, snake_body: SnakeBody) -> None:
        """
        Força o spawn de um tipo específico de comida (para testes)
        
        Args:
            food_type: Tipo de comida a spawnar
            snake_body: Corpo da cobra
        """
        if food_type == EntityType.FOOD_SPECIAL:
            self._spawn_special_food()
        elif food_type == EntityType.FOOD_FUGITIVE:
            self._spawn_fugitive_food()
        else:
            self._spawn_normal_food()
        
        if self._current_food:
            self._current_food.respawn(snake_body)
        
            print(f"🧪 Teste: {food_type.value} forçada")

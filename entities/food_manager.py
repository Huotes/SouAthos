"""
Gerenciador de comidas especiais
Controla spawn, tipos e interações das diferentes comidas
Princípio de responsabilidade única: Apenas gerenciamento de comidas
Versão 2.0: Inclui comida espelho e transformação de fugitivas
"""

import random
import math
from typing import Optional, Union, List
from utils.types import SnakeBody
from entities.food import Food, SpecialFood, FugitiveFood, MirrorFood, EffectParticle
from utils.enums import EntityType
from config.settings import (
    SPECIAL_FOOD_SPAWN_CHANCE, 
    FUGITIVE_FOOD_SPAWN_CHANCE,
    MIRROR_FOOD_SPAWN_CHANCE,
    GRID_SIZE, Effects
)

class FoodManager:
    """
    Gerenciador centralizado das comidas do jogo
    
    Responsabilidades:
    - Controlar spawning de diferentes tipos
    - Gerenciar comida ativa
    - Coordenar interações especiais
    - Estatísticas de comidas consumidas
    - Sistema de transformação fugitiva → normal
    - Efeitos visuais de consumo
    - Gerenciar partículas de efeito
    """
    
    def __init__(self):
        """Inicializa o gerenciador de comidas"""
        self._current_food: Optional[Union[Food, SpecialFood, FugitiveFood, MirrorFood]] = None
        self._effect_particles: List[EffectParticle] = []
        self._spawn_normal_food()
        
        # Estatísticas expandidas
        self._stats = {
            'normal_consumed': 0,
            'special_consumed': 0,
            'fugitive_consumed': 0,
            'mirror_consumed': 0,
            'fugitive_escapes': 0,
            'fugitive_transformations': 0  # Fugitivas que viraram normais
        }
        
        print("🎮 FoodManager v2.0 inicializado!")
        print("🆕 Recursos: Espelho + Transformação de Fugitivas")
    
    @property
    def current_food(self) -> Optional[Union[Food, SpecialFood, FugitiveFood, MirrorFood]]:
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
    
    def _spawn_mirror_food(self) -> None:
        """Spawna comida espelho (inversão de perspectiva)"""
        self._current_food = MirrorFood()
        print("🪞 Comida ESPELHO spawnada! (inverte perspectiva!)")
    
    def _determine_food_type(self) -> EntityType:
        """
        Determina que tipo de comida spawnar baseado nas chances
        
        Returns:
            Tipo de comida a ser spawnada
        """
        rand_value = random.random()
        
        # Ordem de prioridade: Espelho > Fugitiva > Especial > Normal
        if rand_value < MIRROR_FOOD_SPAWN_CHANCE:
            return EntityType.FOOD_MIRROR
        elif rand_value < MIRROR_FOOD_SPAWN_CHANCE + FUGITIVE_FOOD_SPAWN_CHANCE:
            return EntityType.FOOD_FUGITIVE
        elif rand_value < MIRROR_FOOD_SPAWN_CHANCE + FUGITIVE_FOOD_SPAWN_CHANCE + SPECIAL_FOOD_SPAWN_CHANCE:
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
        elif food_type == EntityType.FOOD_MIRROR:
            self._spawn_mirror_food()
        else:
            self._spawn_normal_food()
        
        # Reposiciona evitando a cobra
        if self._current_food:
            self._current_food.respawn(snake_body)
    
    def update(self, delta_time: float, snake_body: SnakeBody) -> None:
        """
        Atualiza a comida atual e efeitos
        
        Args:
            delta_time: Tempo decorrido
            snake_body: Corpo da cobra
        """
        if not self._current_food or not self._current_food.active:
            return
        
        # Atualiza animação da comida
        self._current_food.update_animation(delta_time)
        
        # Atualiza partículas de efeito
        for particle in self._effect_particles[:]:  # Cópia da lista para iteração segura
            particle.update(delta_time)
            if not particle.active:
                self._effect_particles.remove(particle)
        
        # Lógica especial para comida fugitiva
        if isinstance(self._current_food, FugitiveFood):
            # Tenta fugir se cobra estiver próxima
            if self._current_food.try_escape(snake_body):
                self._stats['fugitive_escapes'] += 1
                
                # NOVA MECÂNICA v2.0: Transforma em comida normal após fuga
                self._transform_fugitive_to_normal(snake_body)
    
    def _transform_fugitive_to_normal(self, snake_body: SnakeBody) -> None:
        """
        Transforma comida fugitiva em normal após fuga
        Mecânica v2.0: Torna fugitivas capturáveis após 1 fuga
        
        Args:
            snake_body: Corpo da cobra para evitar
        """
        if isinstance(self._current_food, FugitiveFood):
            # Pega posição atual da fugitiva
            fugitive_position = self._current_food.position
            
            # Cria nova comida normal na mesma posição
            normal_food = Food(EntityType.FOOD_NORMAL)
            normal_food._position = fugitive_position
            normal_food._animation_counter = 0.0
            
            # Substitui a comida atual
            self._current_food = normal_food
            self._stats['fugitive_transformations'] += 1
            
            print("🏃‍♀️ → 🍎 Comida fugitiva virou NORMAL após fuga!")
            print("🎯 Agora você pode capturá-la facilmente!")
    
    def _create_consumption_effect(self, position: tuple, food_type: EntityType) -> None:
        """
        Cria efeito visual para consumo de comida especial
        Sistema v2.0: Partículas coloridas em burst circular
        
        Args:
            position: Posição onde criar o efeito (coordenadas do grid)
            food_type: Tipo de comida consumida
        """
        # Converte posição grid para pixels (centro da célula)
        pixel_x = position[0] * GRID_SIZE + GRID_SIZE // 2
        pixel_y = position[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Determina cor e número de partículas baseado no tipo
        if food_type == EntityType.FOOD_SPECIAL:
            color = (255, 215, 0)  # Dourado
            particle_count = Effects.PARTICLE_BURST_COUNT
            print("✨ Criando efeito dourado...")
            
        elif food_type == EntityType.FOOD_FUGITIVE:
            color = (138, 43, 226)  # Violeta
            particle_count = Effects.PARTICLE_BURST_COUNT
            print("💨 Criando efeito violeta...")
            
        elif food_type == EntityType.FOOD_MIRROR:
            color = (0, 255, 255)  # Ciano
            particle_count = Effects.PARTICLE_BURST_COUNT * 2  # Mais partículas para espelho
            print("🪞 Criando efeito espelho ciano...")
            
        else:
            # Comida normal não tem efeito especial
            return
        
        # Cria burst circular de partículas
        for i in range(particle_count):
            # Calcula ângulo para distribuição uniforme em círculo
            angle = (2 * math.pi * i) / particle_count
            
            # Direção normalizada (x, y)
            direction = (math.cos(angle), math.sin(angle))
            
            # Velocidade aleatória entre 30-80 px/s
            speed = random.uniform(30, 80)
            
            # Cria e adiciona partícula
            particle = EffectParticle((pixel_x, pixel_y), color, direction, speed)
            self._effect_particles.append(particle)
        
        print(f"✨ Burst de {particle_count} partículas criado para {food_type.name}!")
    
    def consume_current_food(self) -> int:
        """
        Consome a comida atual e cria efeitos especiais
        
        Returns:
            Pontos obtidos pela comida
        """
        if not self._current_food or not self._current_food.active:
            return 0
        
        # Captura informações antes do consumo
        points = self._current_food.consume()
        food_position = self._current_food.position
        food_type = self._current_food.entity_type
        
        # Cria efeito visual para comidas especiais
        self._create_consumption_effect(food_position, food_type)
        
        # Atualiza estatísticas e logs detalhados
        if food_type == EntityType.FOOD_NORMAL:
            self._stats['normal_consumed'] += 1
            print(f"🍎 Comida normal consumida! (+{points} pontos)")
            
        elif food_type == EntityType.FOOD_SPECIAL:
            self._stats['special_consumed'] += 1
            print(f"⭐ Comida ESPECIAL consumida! (+{points} pontos) ✨")
            
        elif food_type == EntityType.FOOD_FUGITIVE:
            self._stats['fugitive_consumed'] += 1
            print(f"🏃‍♀️ Comida FUGITIVA capturada! (+{points} pontos) 💨")
            
        elif food_type == EntityType.FOOD_MIRROR:
            self._stats['mirror_consumed'] += 1
            print(f"🪞 Comida ESPELHO consumida! (+{points} pontos) 🔄")
            print("🎭 Prepare-se para a inversão de perspectiva!")
        
        return points
    
    def draw(self, surface) -> None:
        """
        Desenha a comida atual e todos os efeitos visuais
        
        Args:
            surface: Superfície onde desenhar
        """
        # Desenha efeitos de partículas primeiro (camada de fundo)
        for particle in self._effect_particles:
            particle.draw(surface)
        
        # Desenha comida atual por cima dos efeitos
        if self._current_food and self._current_food.active:
            self._current_food.draw(surface)
    
    def get_bounds(self) -> Optional:
        """
        Retorna os limites da comida atual para detecção de colisão
        
        Returns:
            Retângulo da comida ou None se não há comida ativa
        """
        if self._current_food and self._current_food.active:
            return self._current_food.get_bounds()
        return None
    
    def get_position(self) -> Optional:
        """
        Retorna a posição da comida atual
        
        Returns:
            Posição (x, y) da comida ou None se não há comida ativa
        """
        if self._current_food and self._current_food.active:
            return self._current_food.position
        return None
    
    def check_collision(self, other_bounds) -> bool:
        """
        Verifica colisão da comida atual com outro objeto
        
        Args:
            other_bounds: Limites do outro objeto (geralmente a cobra)
            
        Returns:
            True se houver colisão, False caso contrário
        """
        if not self._current_food or not self._current_food.active:
            return False
        
        food_bounds = self._current_food.get_bounds()
        return food_bounds.colliderect(other_bounds) if food_bounds else False
    
    def is_food_active(self) -> bool:
        """
        Verifica se há comida ativa no jogo
        
        Returns:
            True se há comida ativa e disponível para consumo
        """
        return self._current_food is not None and self._current_food.active
    
    def get_food_type(self) -> Optional[EntityType]:
        """
        Retorna o tipo da comida atual
        
        Returns:
            Tipo da comida atual ou None se não há comida
        """
        if self._current_food:
            return self._current_food.entity_type
        return None
    
    def print_statistics(self) -> None:
        """Imprime estatísticas completas de consumo de comidas"""
        total_consumed = sum([
            self._stats['normal_consumed'],
            self._stats['special_consumed'], 
            self._stats['fugitive_consumed'],
            self._stats['mirror_consumed']
        ])
        
        print("\n📊 === ESTATÍSTICAS DE COMIDAS v2.0 ===")
        print(f"🍎 Normais consumidas: {self._stats['normal_consumed']}")
        print(f"⭐ Especiais consumidas: {self._stats['special_consumed']}")
        print(f"🏃‍♀️ Fugitivas capturadas: {self._stats['fugitive_consumed']}")
        print(f"🪞 Espelhos consumidos: {self._stats['mirror_consumed']}")
        print(f"💨 Fugas bem-sucedidas: {self._stats['fugitive_escapes']}")
        print(f"🔄 Fugitivas → Normais: {self._stats['fugitive_transformations']}")
        print(f"🎯 Total de comidas: {total_consumed}")
        
        if total_consumed > 0:
            # Calcula taxas percentuais
            special_rate = (self._stats['special_consumed'] / total_consumed) * 100
            fugitive_rate = (self._stats['fugitive_consumed'] / total_consumed) * 100
            mirror_rate = (self._stats['mirror_consumed'] / total_consumed) * 100
            
            print(f"\n📈 === TAXAS DE CONSUMO ===")
            print(f"⭐ Taxa de especiais: {special_rate:.1f}%")
            print(f"🏃‍♀️ Taxa de fugitivas: {fugitive_rate:.1f}%")
            print(f"🪞 Taxa de espelhos: {mirror_rate:.1f}%")
            
            # Estatísticas avançadas
            if self._stats['fugitive_escapes'] > 0:
                transformation_rate = (self._stats['fugitive_transformations'] / self._stats['fugitive_escapes']) * 100
                print(f"🔄 Taxa transformação fugitivas: {transformation_rate:.1f}%")
        
        print("=" * 40)
    
    def reset(self) -> None:
        """Reseta o gerenciador para estado inicial"""
        print("🔄 Resetando FoodManager...")
        
        # Reseta comida atual
        if self._current_food:
            self._current_food.deactivate()
        
        # Spawna nova comida normal
        self._spawn_normal_food()
        
        # Limpa todas as estatísticas
        self._stats = {
            'normal_consumed': 0,
            'special_consumed': 0,
            'fugitive_consumed': 0,
            'mirror_consumed': 0,
            'fugitive_escapes': 0,
            'fugitive_transformations': 0
        }
        
        # Limpa todos os efeitos visuais
        self._effect_particles.clear()
        
        print("✅ FoodManager resetado com sucesso!")
    
    def force_spawn_type(self, food_type: EntityType, snake_body: SnakeBody) -> None:
        """
        Força o spawn de um tipo específico de comida (para testes e debugging)
        
        Args:
            food_type: Tipo de comida a spawnar
            snake_body: Corpo da cobra para evitar spawnar em cima
        """
        print(f"🧪 === TESTE: FORÇANDO SPAWN DE {food_type.name} ===")
        
        if food_type == EntityType.FOOD_SPECIAL:
            self._spawn_special_food()
        elif food_type == EntityType.FOOD_FUGITIVE:
            self._spawn_fugitive_food()
        elif food_type == EntityType.FOOD_MIRROR:
            self._spawn_mirror_food()
        else:
            self._spawn_normal_food()
        
        # Reposiciona evitando a cobra
        if self._current_food:
            self._current_food.respawn(snake_body)
        
        print(f"✅ {food_type.name} spawnada com sucesso!")
    
    def get_effect_particles_count(self) -> int:
        """
        Retorna o número atual de partículas de efeito ativas
        
        Returns:
            Número de partículas ativas
        """
        return len([p for p in self._effect_particles if p.active])
    
    def clear_all_effects(self) -> None:
        """Limpa todos os efeitos visuais ativos"""
        self._effect_particles.clear()
        print("🧹 Todos os efeitos visuais foram limpos")
    
    def get_detailed_stats(self) -> dict:
        """
        Retorna estatísticas detalhadas para análise
        
        Returns:
            Dicionário com estatísticas expandidas
        """
        total_consumed = sum([
            self._stats['normal_consumed'],
            self._stats['special_consumed'], 
            self._stats['fugitive_consumed'],
            self._stats['mirror_consumed']
        ])
        
        return {
            **self._stats,
            'total_consumed': total_consumed,
            'active_particles': self.get_effect_particles_count(),
            'current_food_type': self.get_food_type().name if self.get_food_type() else None,
            'food_active': self.is_food_active()
        }

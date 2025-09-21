"""
Engine principal do jogo
Princípios: SOLID, responsabilidade única, controle centralizado
Inclui sistema de níveis, velocidade dinâmica e efeitos visuais
"""

import pygame
import sys
from typing import Optional
from utils.enums import GameState, Direction
from utils.types import Clock
from entities.snake import Snake
from entities.food_manager import FoodManager
from graphics.renderer import Renderer
from graphics.ui import UIManager
from core.events import EventManager, game_events
from config.settings import (
    BASE_FPS, MAX_FPS, FPS_INCREASE_PER_LEVEL, INITIAL_SNAKE_X, INITIAL_SNAKE_Y, 
    POINTS_PER_FOOD, POINTS_PER_LEVEL, Effects
)

class GameEngine:
    """
    Engine principal do jogo Snake
    
    Responsabilidades:
    - Controle do loop principal
    - Gerenciamento de estados
    - Coordenação entre sistemas
    - Lógica de jogo de alto nível
    - Sistema de níveis e progressão
    - Controle de velocidade dinâmica
    - Efeitos visuais de level up
    """
    
    def __init__(self):
        """Inicializa o engine do jogo"""
        # Inicialização do pygame
        pygame.init()
        
        # Sistemas principais
        self._renderer = Renderer()
        self._ui_manager = UIManager()
        self._event_manager = EventManager()
        self._clock = pygame.time.Clock()
        
        # Estado do jogo
        self._current_state = GameState.PLAYING
        self._score = 0
        self._level = 1
        self._current_fps = BASE_FPS
        
        # Sistema de nível e efeitos
        self._level_up_notification_timer = 0.0
        self._show_level_up_notification = False
        self._last_level = 1  # Para detectar mudanças de nível
        
        # Entidades do jogo
        self._snake = Snake((INITIAL_SNAKE_X, INITIAL_SNAKE_Y))
        self._food_manager = FoodManager()
        
        # Controle de pausa
        self._paused = False
        
        # Controle de tempo para efeitos
        self._delta_time = 0.0
        self._last_time = pygame.time.get_ticks()
        
        # Setup de eventos
        self._setup_event_listeners()
        
        print("🐍 Snake Game Engine Inicializado!")
        self._print_controls()
        self._print_game_info()
    
    def _setup_event_listeners(self) -> None:
        """Configura os listeners de eventos do jogo"""
        # Eventos de gameplay
        game_events.subscribe('food_eaten', self._on_food_eaten)
        game_events.subscribe('snake_collision', self._on_snake_collision)
        game_events.subscribe('game_restart', self._on_game_restart)
    
    def _print_controls(self) -> None:
        """Imprime os controles do jogo"""
        print("=== CONTROLES ===")
        print("🎮 Movimento: Setas ou WASD")
        print("⏸️  Pausar: SPACE")
        print("🔄 Reiniciar: R (após game over)")
        print("❌ Sair: Q ou fechar janela")
        print("==================")
    
    def _print_game_info(self) -> None:
        """Imprime informações sobre as novas features"""
        print("\n=== NOVAS FEATURES ===")
        print("🍎 Pontuação: +1 ponto por fruta normal")
        print("⭐ Especiais: +5 pontos (contorno dourado)")
        print("🏃‍♀️ Fugitivas: +3 pontos (pisca e foge!)")
        print("🚀 Níveis: A cada 10 pontos")
        print("⚡ Velocidade: Aumenta automaticamente")
        print("🌈 Efeitos: Grid colorido no level up")
        print("📊 Sistema de comidas especiais ativo!")
        print("=======================")
    
    def _calculate_delta_time(self) -> None:
        """Calcula o tempo decorrido desde o último frame"""
        current_time = pygame.time.get_ticks()
        self._delta_time = (current_time - self._last_time) / 1000.0  # Converter para segundos
        self._last_time = current_time
    
    def _handle_input(self) -> None:
        """Processa entrada do usuário"""
        actions = self._event_manager.process_events()
        
        for action in actions:
            if action == 'quit':
                self._current_state = GameState.QUIT
            
            elif action == 'pause':
                if self._current_state == GameState.PLAYING:
                    self._paused = not self._paused
                    print(f"⏸️ Jogo {'pausado' if self._paused else 'despausado'}")
            
            elif action == 'restart':
                if self._current_state == GameState.GAME_OVER:
                    game_events.dispatch('game_restart')
            
            elif self._current_state == GameState.PLAYING and not self._paused:
                # Movimento da cobra
                direction = self._event_manager.get_direction_from_action(action)
                if direction:
                    self._snake.change_direction(direction)
    
    def _update_game_logic(self) -> None:
        """Atualiza a lógica do jogo"""
        if (self._current_state != GameState.PLAYING or 
            self._paused or 
            not self._snake.active):
            return
        
        # Calcula delta time
        self._calculate_delta_time()
        
        # Atualiza efeitos visuais do renderer
        self._renderer.update_effects(self._delta_time)
        
        # Atualiza timer da notificação de level up
        if self._show_level_up_notification:
            self._level_up_notification_timer -= self._delta_time
            if self._level_up_notification_timer <= 0:
                self._show_level_up_notification = False
                print("✨ Notificação de level up removida")
        
        # Move a cobra
        self._snake.move()
        
        # Verifica colisões
        self._check_collisions()
        
        # Atualiza sistema de comidas
        self._food_manager.update(self._delta_time, self._snake.body)
    
    def _check_collisions(self) -> None:
        """Verifica todas as colisões do jogo"""
        # Colisão com paredes
        if self._snake.check_wall_collision():
            game_events.dispatch('snake_collision', collision_type='wall')
            return
        
        # Colisão consigo mesma
        if self._snake.check_self_collision():
            game_events.dispatch('snake_collision', collision_type='self')
            return
        
        # Colisão com comida
        if self._food_manager.check_collision(self._snake.get_bounds()):
            # Consome a comida atual
            points_gained = self._food_manager.consume_current_food()
            food_type = self._food_manager.get_food_type()
            
            # Dispatcha evento com informações da comida
            game_events.dispatch('food_eaten', 
                               points=points_gained,
                               food_type=food_type,
                               snake_body=self._snake.body)
    
    def _render_game(self) -> None:
        """Renderiza todos os elementos do jogo"""
        # Limpa a tela
        self._renderer.clear_screen()
        
        # Desenha o grid de fundo (transparente com efeitos)
        self._renderer.draw_grid()
        
        # Desenha entidades do jogo
        self._food_manager.draw(self._renderer.screen)
        
        if self._snake.active:
            self._snake.draw(self._renderer.screen)
        
        # Desenha UI
        self._render_ui()
        
        # Atualiza display
        self._renderer.present()
    
    def _render_ui(self) -> None:
        """Renderiza a interface do usuário"""
        # Calcula multiplicador de velocidade para exibição
        speed_multiplier = self._current_fps / BASE_FPS
        
        # HUD sempre visível (com informações atualizadas)
        self._ui_manager.draw_hud(
            self._renderer.screen, 
            self._score, 
            self._snake.length,
            self._level,
            speed_multiplier,
            self._food_manager.stats
        )
        
        # Notificação de level up (centralizada na tela)
        if self._show_level_up_notification:
            self._ui_manager.draw_level_up_notification(
                self._renderer.screen,
                self._level
            )
        
        # Overlays baseados no estado
        if self._current_state == GameState.GAME_OVER:
            self._ui_manager.draw_game_over_screen(
                self._renderer.screen, 
                self._score
            )
        
        elif self._paused:
            self._ui_manager.draw_pause_screen(self._renderer.screen)
    
    def _calculate_level_from_score(self) -> int:
        """
        Calcula o nível baseado na pontuação atual
        
        Returns:
            Nível atual baseado no score
        """
        return (self._score // POINTS_PER_LEVEL) + 1
    
    def _calculate_fps_for_level(self, level: int) -> float:
        """
        Calcula o FPS para um determinado nível
        
        Args:
            level: Nível para calcular FPS
            
        Returns:
            FPS calculado para o nível
        """
        calculated_fps = BASE_FPS * (FPS_INCREASE_PER_LEVEL ** (level - 1))
        return min(MAX_FPS, calculated_fps)
    
    def _on_food_eaten(self, points: int, food_type, snake_body: list) -> None:
        """
        Callback quando comida é consumida
        
        Args:
            points: Pontos obtidos
            food_type: Tipo da comida consumida
            snake_body: Corpo atual da cobra
        """
        # Atualiza score baseado nos pontos da comida
        old_score = self._score
        self._score += points
        
        # Calcula novo nível baseado no score
        new_level = self._calculate_level_from_score()
        
        # Verifica se subiu de nível
        if new_level > self._level:
            self._level_up(new_level)
        
        # Cresce a cobra
        self._snake.grow()
        
        # Spawna nova comida (evita corpo da cobra)
        self._food_manager.spawn_new_food(snake_body)
        
        # Log baseado no tipo de comida
        if food_type.name == 'FOOD_SPECIAL':
            print(f"⭐ Comida especial consumida! {old_score} → {self._score} pontos")
        elif food_type.name == 'FOOD_FUGITIVE':
            print(f"🏃‍♀️ Comida fugitiva capturada! {old_score} → {self._score} pontos")
        else:
            print(f"🍎 Comida normal consumida! {old_score} → {self._score} pontos")
        
        # Mostra progresso para próximo nível
        if new_level <= self._level:
            points_to_next = POINTS_PER_LEVEL - (self._score % POINTS_PER_LEVEL)
            print(f"🎯 Próximo nível em {points_to_next} pontos")
    
    def _level_up(self, new_level: int) -> None:
        """
        Processa subida de nível
        
        Args:
            new_level: Novo nível alcançado
        """
        old_level = self._level
        old_fps = self._current_fps
        
        # Atualiza nível
        self._level = new_level
        
        # Calcula nova velocidade (FPS)
        self._current_fps = self._calculate_fps_for_level(self._level)
        
        # Ativa efeitos visuais
        self._renderer.start_level_up_effect()
        
        # Mostra notificação na tela
        self._show_level_up_notification = True
        self._level_up_notification_timer = 2.5  # 2.5 segundos na tela
        
        # Calcula multiplicador de velocidade
        speed_multiplier = self._current_fps / BASE_FPS
        
        # Log celebratório
        print(f"\n🎉 === LEVEL UP! === 🎉")
        print(f"📈 Nível: {old_level} → {new_level}")
        print(f"⚡ FPS: {old_fps:.1f} → {self._current_fps:.1f}")
        print(f"🚀 Velocidade: {speed_multiplier:.2f}x")
        print(f"🌈 Efeito visual ativo por {Effects.LEVEL_UP_FLASH_DURATION}s")
        print(f"🎯 Próximo nível em {POINTS_PER_LEVEL} pontos")
        print("=" * 25 + "\n")
    
    def _on_snake_collision(self, collision_type: str) -> None:
        """
        Callback quando cobra colide
        
        Args:
            collision_type: Tipo de colisão ('wall' ou 'self')
        """
        # Calcula estatísticas finais
        final_speed = self._current_fps / BASE_FPS
        
        # Mostra estatísticas de comidas
        self._food_manager.print_statistics()
        
        print(f"\n💀 === GAME OVER === 💀")
        print(f"☠️ Causa: Colisão com {'parede' if collision_type == 'wall' else 'próprio corpo'}")
        print(f"📊 Score final: {self._score} pontos")
        print(f"🎯 Nível alcançado: {self._level}")
        print(f"📏 Tamanho final: {self._snake.length} segmentos")
        print(f"⚡ Velocidade final: {self._current_fps:.1f} FPS ({final_speed:.2f}x)")
        print("=" * 25 + "\n")
        
        # Muda estado para game over
        self._current_state = GameState.GAME_OVER
        self._snake.deactivate()
    
    def _on_game_restart(self) -> None:
        """Callback para reiniciar o jogo"""
        print("🔄 === REINICIANDO JOGO === 🔄")
        
        # Reseta entidades
        self._snake.reset((INITIAL_SNAKE_X, INITIAL_SNAKE_Y))
        self._food_manager.reset()
        
        # Reseta estado do jogo
        self._score = 0
        self._level = 1
        self._current_fps = BASE_FPS
        self._paused = False
        self._current_state = GameState.PLAYING
        
        # Reseta efeitos visuais
        self._show_level_up_notification = False
        self._level_up_notification_timer = 0.0
        self._last_level = 1
        
        # Reseta tempo
        self._last_time = pygame.time.get_ticks()
        
        print("✅ Jogo reiniciado com sucesso!")
        print(f"🎮 Estado inicial: Nível 1, {BASE_FPS} FPS")
        print("🎯 Colete 10 frutas para o primeiro level up!")
        print("=" * 35 + "\n")
    
    def _print_current_status(self) -> None:
        """Imprime status atual do jogo (debug)"""
        if self._current_state == GameState.PLAYING and not self._paused:
            speed_mult = self._current_fps / BASE_FPS
            points_to_next = POINTS_PER_LEVEL - (self._score % POINTS_PER_LEVEL)
            
            print(f"📊 Status: Score {self._score} | Nível {self._level} | " +
                  f"Velocidade {speed_mult:.2f}x | Próximo nível em {points_to_next}")
    
    def run(self) -> None:
        """
        Loop principal do jogo
        
        Implementa o padrão Game Loop otimizado:
        1. Processar entrada
        2. Atualizar lógica  
        3. Renderizar
        4. Controlar framerate dinâmico
        """
        print("🚀 Iniciando Snake Game com features avançadas...")
        print("🌈 Grid transparente e efeitos visuais ativados!")
        print("⚡ Sistema de velocidade dinâmica configurado!")
        
        try:
            while (self._event_manager.is_running() and 
                   self._current_state != GameState.QUIT):
                
                # 1. Processar entrada do usuário
                self._handle_input()
                
                # 2. Atualizar lógica do jogo
                self._update_game_logic()
                
                # 3. Renderizar todos os elementos
                self._render_game()
                
                # 4. Controlar framerate (dinâmico baseado no nível)
                self._clock.tick(self._current_fps)
        
        except KeyboardInterrupt:
            print("\n⏹️ Jogo interrompido pelo usuário")
        
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            self._cleanup()
    
    def _cleanup(self) -> None:
        """Limpa recursos e finaliza o jogo"""
        print("🧹 Limpando recursos do game engine...")
        
        # Cleanup dos sistemas
        self._renderer.cleanup()
        self._ui_manager.cleanup()
        
        # Finaliza pygame
        pygame.quit()
        
        print("👋 Snake Game Engine finalizado com sucesso!")
    
    # Properties para acesso ao estado do jogo
    @property
    def score(self) -> int:
        """Retorna o score atual"""
        return self._score
    
    @property
    def game_state(self) -> GameState:
        """Retorna o estado atual do jogo"""
        return self._current_state
    
    @property
    def level(self) -> int:
        """Retorna o nível atual"""
        return self._level
    
    @property
    def current_fps(self) -> float:
        """Retorna o FPS atual"""
        return self._current_fps
    
    @property
    def speed_multiplier(self) -> float:
        """Retorna o multiplicador de velocidade atual"""
        return self._current_fps / BASE_FPS
    
    @property
    def is_paused(self) -> bool:
        """Retorna se o jogo está pausado"""
        return self._paused
    
    @property
    def points_to_next_level(self) -> int:
        """Retorna quantos pontos faltam para o próximo nível"""
        return POINTS_PER_LEVEL - (self._score % POINTS_PER_LEVEL)
    
    @property
    def total_fruits_eaten(self) -> int:
        """Retorna o total de frutas consumidas"""
        return self._score  # Como cada fruta vale 1 ponto

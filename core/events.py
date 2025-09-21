"""
Sistema de eventos centralizados
Princípio DRY: Centraliza lógica de eventos
Princípio de responsabilidade única: Apenas eventos
"""

import pygame
from typing import Dict, List, Callable, Optional
from utils.enums import Direction, GameState
from utils.types import Event
from config.settings import Controls

class EventManager:
    """
    Gerenciador centralizado de eventos
    
    Responsabilidades:
    - Processamento de eventos pygame
    - Mapeamento de teclas para ações
    - Sistema de callbacks
    - Controle de estado do jogo
    """
    
    def __init__(self):
        """Inicializa o gerenciador de eventos"""
        self._event_callbacks: Dict[int, List[Callable]] = {}
        self._key_mappings = self._setup_key_mappings()
        self._running = True
    
    def _setup_key_mappings(self) -> Dict[int, str]:
        """
        Configura o mapeamento de teclas
        
        Returns:
            Dicionário com mapeamento tecla -> ação
        """
        mappings = {}
        
        # Movimento
        for key_name in Controls.MOVE_UP:
            key_code = getattr(pygame, key_name)
            mappings[key_code] = 'move_up'
        
        for key_name in Controls.MOVE_DOWN:
            key_code = getattr(pygame, key_name)
            mappings[key_code] = 'move_down'
        
        for key_name in Controls.MOVE_LEFT:
            key_code = getattr(pygame, key_name)
            mappings[key_code] = 'move_left'
        
        for key_name in Controls.MOVE_RIGHT:
            key_code = getattr(pygame, key_name)
            mappings[key_code] = 'move_right'
        
        # Ações
        mappings[getattr(pygame, Controls.RESTART)] = 'restart'
        mappings[getattr(pygame, Controls.QUIT)] = 'quit'
        mappings[getattr(pygame, Controls.PAUSE)] = 'pause'
        
        return mappings
    
    def register_callback(self, event_type: int, callback: Callable) -> None:
        """
        Registra um callback para um tipo de evento
        
        Args:
            event_type: Tipo do evento (pygame.KEYDOWN, etc.)
            callback: Função callback
        """
        if event_type not in self._event_callbacks:
            self._event_callbacks[event_type] = []
        
        self._event_callbacks[event_type].append(callback)
    
    def unregister_callback(self, event_type: int, callback: Callable) -> None:
        """
        Remove um callback
        
        Args:
            event_type: Tipo do evento
            callback: Função callback a remover
        """
        if event_type in self._event_callbacks:
            try:
                self._event_callbacks[event_type].remove(callback)
            except ValueError:
                pass  # Callback não encontrado
    
    def process_events(self) -> List[str]:
        """
        Processa todos os eventos da fila
        
        Returns:
            Lista de ações identificadas
        """
        actions = []
        
        for event in pygame.event.get():
            # Executa callbacks registrados
            if event.type in self._event_callbacks:
                for callback in self._event_callbacks[event.type]:
                    callback(event)
            
            # Processa eventos padrão
            if event.type == pygame.QUIT:
                self._running = False
                actions.append('quit')
            
            elif event.type == pygame.KEYDOWN:
                action = self._key_mappings.get(event.key)
                if action:
                    actions.append(action)
        
        return actions
    
    def get_direction_from_action(self, action: str) -> Optional[Direction]:
        """
        Converte ação em direção
        
        Args:
            action: Ação identificada
            
        Returns:
            Direção correspondente ou None
        """
        direction_map = {
            'move_up': Direction.UP,
            'move_down': Direction.DOWN,
            'move_left': Direction.LEFT,
            'move_right': Direction.RIGHT
        }
        
        return direction_map.get(action)
    
    def is_running(self) -> bool:
        """
        Verifica se o jogo deve continuar executando
        
        Returns:
            True se deve continuar, False para sair
        """
        return self._running
    
    def stop(self) -> None:
        """Para a execução do jogo"""
        self._running = False
    
    def reset(self) -> None:
        """Reseta o estado do gerenciador"""
        self._running = True

class GameEventDispatcher:
    """
    Despachador de eventos específicos do jogo
    
    Facilita comunicação entre componentes
    """
    
    def __init__(self):
        """Inicializa o despachador"""
        self._listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Inscreve um callback para um evento
        
        Args:
            event_name: Nome do evento
            callback: Função callback
        """
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        
        self._listeners[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """
        Remove inscrição de um callback
        
        Args:
            event_name: Nome do evento
            callback: Função callback
        """
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass
    
    def dispatch(self, event_name: str, **kwargs) -> None:
        """
        Despacha um evento para todos os listeners
        
        Args:
            event_name: Nome do evento
            **kwargs: Argumentos do evento
        """
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                try:
                    callback(**kwargs)
                except Exception as e:
                    print(f"Erro no callback do evento {event_name}: {e}")

# Instância global do despachador (Singleton pattern)
game_events = GameEventDispatcher()

#!/usr/bin/env python3
"""
Snake Game - Ponto de entrada principal
Arquitetura modular seguindo princípios DRY, KISS e POO

Estrutura do projeto:
- config/: Configurações centralizadas
- core/: Engine e sistemas principais  
- entities/: Objetos do jogo (Snake, Food)
- graphics/: Sistema de renderização e UI
- utils/: Utilitários e tipos compartilhados

Autor: Snake Game Development Team
Versão: 1.0.0
Python: 3.13+
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Adiciona o diretório raiz ao path para imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_python_version() -> bool:
    """
    Verifica se a versão do Python é compatível
    
    Returns:
        True se versão é compatível, False caso contrário
    """
    if sys.version_info < (3, 9):
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} não suportado")
        print("💡 Requer Python 3.9 ou superior")
        print("📥 Baixe em: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detectado")
    return True

def check_dependencies() -> bool:
    """
    Verifica se todas as dependências estão instaladas
    
    Returns:
        True se tudo ok, False se falta algo
    """
    missing_deps = []
    
    # Verifica pygame
    try:
        import pygame
        print(f"✅ Pygame {pygame.version.ver} detectado")
    except ImportError:
        missing_deps.append("pygame")
    
    # Verifica typing_extensions (para Python < 3.10)
    if sys.version_info < (3, 10):
        try:
            import typing_extensions
            print("✅ typing_extensions detectado")
        except ImportError:
            missing_deps.append("typing_extensions")
    
    if missing_deps:
        print("❌ Dependências não encontradas:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 Instale com:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("   ou")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_project_structure() -> bool:
    """
    Verifica se a estrutura do projeto está correta
    
    Returns:
        True se estrutura ok, False caso contrário
    """
    required_dirs = ['config', 'core', 'entities', 'graphics', 'utils']
    required_files = [
        'config/settings.py',
        'core/__init__.py',
        'core/game_engine.py', 
        'core/events.py',
        'entities/__init__.py',
        'entities/game_object.py',
        'entities/snake.py',
        'entities/food.py',
        'graphics/__init__.py',
        'graphics/renderer.py',
        'graphics/ui.py',
        'utils/__init__.py',
        'utils/enums.py',
        'utils/types.py'
    ]
    
    missing_items = []
    
    # Verifica diretórios
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists() or not dir_path.is_dir():
            missing_items.append(f"Diretório: {dir_name}/")
    
    # Verifica arquivos
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists() or not full_path.is_file():
            missing_items.append(f"Arquivo: {file_path}")
    
    if missing_items:
        print("❌ Estrutura do projeto incompleta:")
        for item in missing_items:
            print(f"   • {item}")
        print("\n💡 Certifique-se de ter todos os módulos na estrutura correta")
        return False
    
    print("✅ Estrutura do projeto verificada")
    return True

def import_game_modules() -> Optional[object]:
    """
    Importa os módulos do jogo com tratamento de erros
    
    Returns:
        Classe GameEngine se sucesso, None se erro
    """
    try:
        from core.game_engine import GameEngine
        print("✅ Módulos do jogo importados com sucesso")
        return GameEngine
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos do jogo: {e}")
        print("🔧 Verifique se todos os arquivos estão no local correto")
        return None
    
    except Exception as e:
        print(f"💥 Erro inesperado durante import: {e}")
        return None

def print_welcome_banner() -> None:
    """Imprime o banner de boas-vindas"""
    banner = """
╔══════════════════════════════════════════╗
║           🐍 SNAKE GAME 🐍               ║
║                                          ║
║        Arquitetura Modular POO           ║
║       Python 3.13 + Pygame             ║
╚══════════════════════════════════════════╝
"""
    print(banner)

def print_project_info() -> None:
    """Imprime informações sobre a estrutura do projeto"""
    print("\n📋 ARQUITETURA MODULAR:")
    print("┌── main.py              # Ponto de entrada")
    print("├── config/")
    print("│   └── settings.py      # Configurações centralizadas")
    print("├── core/")
    print("│   ├── game_engine.py   # Engine principal do jogo")
    print("│   └── events.py        # Sistema de eventos")
    print("├── entities/")
    print("│   ├── game_object.py   # Classe base abstrata")
    print("│   ├── snake.py         # Lógica da cobra")
    print("│   └── food.py          # Lógica da comida")
    print("├── graphics/")
    print("│   ├── renderer.py      # Sistema de renderização")
    print("│   └── ui.py           # Interface do usuário")
    print("└── utils/")
    print("    ├── enums.py        # Enumerações do jogo")
    print("    └── types.py        # Type hints personalizados")
    
    print("\n🎯 PRINCÍPIOS APLICADOS:")
    print("• DRY: Configurações centralizadas, sem duplicação de código")
    print("• KISS: Módulos simples com responsabilidades bem definidas") 
    print("• POO: Herança, encapsulamento, polimorfismo e abstração")
    print("• SOLID: Responsabilidade única e alta extensibilidade")

def print_game_controls() -> None:
    """Imprime os controles do jogo"""
    print("\n🎮 CONTROLES DO JOGO:")
    print("┌─────────────────────────────────────┐")
    print("│ 🎯 Movimento: ↑↓←→ ou WASD          │")
    print("│ ⏸️  Pausar:   SPACE                  │") 
    print("│ 🔄 Reiniciar: R (após game over)    │")
    print("│ ❌ Sair:     Q ou fechar janela     │")
    print("└─────────────────────────────────────┘")

def main() -> int:
    """
    Função principal do jogo
    
    Returns:
        Código de saída (0 = sucesso, 1 = erro)
    """
    # Banner de boas-vindas
    print_welcome_banner()
    
    print("🔍 Verificando sistema...")
    
    # 1. Verificar versão do Python
    if not check_python_version():
        return 1
    
    # 2. Verificar dependências
    if not check_dependencies():
        return 1
    
    # 3. Verificar estrutura do projeto
    if not check_project_structure():
        return 1
    
    # 4. Importar módulos do jogo
    GameEngine = import_game_modules()
    if GameEngine is None:
        return 1
    
    # Informações do projeto
    print_project_info()
    print_game_controls()
    
    print("\n" + "="*50)
    print("🚀 INICIANDO SNAKE GAME...")
    print("="*50)
    
    try:
        # Inicializa e executa o jogo
        engine = GameEngine()
        engine.run()
        
        print("\n✅ Jogo finalizado com sucesso!")
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Jogo interrompido pelo usuário (Ctrl+C)")
        return 0
        
    except Exception as e:
        print(f"\n💥 Erro crítico durante execução:")
        print(f"   {type(e).__name__}: {e}")
        print("\n🐛 Possíveis causas:")
        print("   • Arquivo de configuração corrompido")
        print("   • Problema com pygame/display")
        print("   • Recurso do sistema indisponível")
        print("   • Bug no código do jogo")
        
        # Em modo debug, mostra traceback completo
        if '--debug' in sys.argv or '-d' in sys.argv:
            import traceback
            print("\n📋 TRACEBACK COMPLETO:")
            traceback.print_exc()
        
        return 1

def show_help() -> None:
    """Mostra ajuda sobre como usar o programa"""
    help_text = """
🐍 Snake Game - Ajuda

USO:
    python main.py [opções]

OPÇÕES:
    -h, --help     Mostra esta ajuda
    -d, --debug    Ativa modo debug (mostra traceback completo)
    -v, --version  Mostra versão do jogo
    --check        Apenas verifica dependências (não executa)

EXEMPLOS:
    python main.py              # Executa o jogo normalmente
    python main.py --debug      # Executa com debug ativado
    python main.py --check      # Verifica se tudo está ok

REQUISITOS:
    • Python 3.9+
    • pygame 2.5.0+
    • typing_extensions (para Python < 3.10)

ESTRUTURA:
    Certifique-se de que todos os módulos estejam organizados
    na estrutura de diretórios correta conforme documentação.
    
Para mais informações, consulte o README.md
"""
    print(help_text)

def show_version() -> None:
    """Mostra informações de versão"""
    print("🐍 Snake Game")
    print("Versão: 1.0.0")
    print("Arquitetura: Modular POO")
    print(f"Python: {sys.version}")
    
    try:
        import pygame
        print(f"Pygame: {pygame.version.ver}")
    except ImportError:
        print("Pygame: Não instalado")

if __name__ == "__main__":
    # Processa argumentos da linha de comando
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['-h', '--help']:
            show_help()
            sys.exit(0)
        
        elif arg in ['-v', '--version']:
            show_version()
            sys.exit(0)
        
        elif arg == '--check':
            print("🔍 Verificando sistema...")
            success = (check_python_version() and 
                      check_dependencies() and 
                      check_project_structure())
            
            if success:
                print("✅ Tudo pronto para executar o jogo!")
                sys.exit(0)
            else:
                print("❌ Sistema não está pronto")
                sys.exit(1)
    
    # Executa o jogo
    exit_code = main()
    sys.exit(exit_code)

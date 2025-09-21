"""
Configuração do projeto Snake Game
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lê o README para a descrição longa
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="snake-game-modular",
    version="1.0.0",
    description="Jogo Snake modular em Python 3.13 com Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Snake Game Development Team",
    author_email="dev@snakegame.com",
    url="https://github.com/usuario/snake-game-modular",
    
    # Estrutura do projeto
    packages=find_packages(),
    include_package_data=True,
    
    # Dependências
    install_requires=[
        "pygame>=2.5.0",
        "typing-extensions>=4.0.0",
    ],
    
    # Versão mínima do Python
    python_requires=">=3.9",
    
    # Classificadores
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    
    # Keywords
    keywords="snake game pygame python modular oop dry kiss",
    
    # Ponto de entrada
    entry_points={
        "console_scripts": [
            "snake-game=main:main",
        ],
    },
    
    # Metadados extras
    project_urls={
        "Bug Reports": "https://github.com/usuario/snake-game-modular/issues",
        "Source": "https://github.com/usuario/snake-game-modular",
        "Documentation": "https://github.com/usuario/snake-game-modular/wiki",
    },
)

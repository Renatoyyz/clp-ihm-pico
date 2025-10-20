#!/usr/bin/env python3
"""
🥧 RASPBERRY PI PICO FILE UPLOADER
==========================================
Interface principal do projeto CLP-IHM-PICO

Este é o ponto de entrada principal do projeto.
A aplicação real está em src/universal_uploader.py

Autor: Projeto CLP-IHM-PICO
Data: Outubro 2025
"""

import sys
import os

# Adiciona a pasta src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa a aplicação principal
if __name__ == "__main__":
    try:
        from universal_uploader import main
        main()
    except ImportError as e:
        print("❌ Erro ao importar universal_uploader:")
        print(f"   {e}")
        print("💡 Certifique-se de que o arquivo src/universal_uploader.py existe")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Aplicação interrompida pelo usuário")
        sys.exit(0)
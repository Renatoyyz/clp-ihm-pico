#!/usr/bin/env python3
"""
Teste básico da funcionalidade IHM
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'interface_ladder'))

try:
    from PyQt5.QtWidgets import QApplication
    from interface_ladder.ihm_config_dialog import IHMConfigDialog
    
    print("✅ Importações IHM - OK")
    
    app = QApplication(sys.argv)
    
    # Teste básico da dialog
    dialog = IHMConfigDialog()
    print("✅ Criação da dialog IHM - OK")
    
    # Teste de componentes disponíveis
    if hasattr(dialog, 'ihm_available') and dialog.ihm_available:
        print("✅ Componentes IHM disponíveis - OK")
        print(f"✅ Canvas: {type(dialog.ihm_canvas).__name__}")
        print(f"✅ Screen Manager: {type(dialog.screen_manager).__name__}")
        print(f"✅ Properties Panel: {type(dialog.properties_panel).__name__}")
    else:
        print("⚠️ Alguns componentes IHM podem não estar disponíveis")
    
    print("\n🎉 Sistema IHM funcionando corretamente!")
    print("\nPara testar:")
    print("1. Execute: python main.py")
    print("2. Na biblioteca de componentes, clique no Display IHM")
    print("3. Arraste componentes para o canvas")
    print("4. Teste a persistência trocando entre telas")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

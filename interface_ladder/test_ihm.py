#!/usr/bin/env python3
"""
Teste simples do sistema IHM
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

# Testar imports
try:
    from ihm_components import IHMComponentLibrary
    print("✅ ihm_components importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar ihm_components: {e}")
    sys.exit(1)

try:
    from ihm_screen_manager import IHMScreenManager  
    print("✅ ihm_screen_manager importado com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar ihm_screen_manager: {e}")
    sys.exit(1)

def test_ihm_components():
    """Teste básico dos componentes IHM"""
    app = QApplication(sys.argv)
    
    # Janela principal simples
    window = QMainWindow()
    window.setWindowTitle("Teste IHM Simples")
    window.setGeometry(100, 100, 800, 600)
    
    # Widget central
    central = QWidget()
    layout = QHBoxLayout(central)
    
    try:
        # Teste biblioteca de componentes
        print("🔄 Criando biblioteca de componentes...")
        library = IHMComponentLibrary()
        layout.addWidget(library, 1)
        print("✅ Biblioteca criada com sucesso")
        
        # Teste gerenciador de telas
        print("🔄 Criando gerenciador de telas...")
        manager = IHMScreenManager()
        layout.addWidget(manager, 1)
        print("✅ Gerenciador criado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro ao criar componentes: {e}")
        return False
    
    window.setCentralWidget(central)
    window.show()
    
    print("🚀 Aplicação teste iniciada com sucesso!")
    print("Feche a janela para encerrar o teste.")
    
    app.exec_()
    return True

if __name__ == "__main__":
    test_ihm_components()
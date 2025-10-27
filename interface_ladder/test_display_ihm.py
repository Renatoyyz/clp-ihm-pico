#!/usr/bin/env python3
"""
Teste do Bloco Display IHM
Verificar se o componente foi integrado corretamente
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from component_library import ComponentLibrary

def test_display_ihm():
    """Testar o componente Display IHM"""
    
    app = QApplication(sys.argv)
    
    # Criar janela de teste
    window = QMainWindow()
    window.setWindowTitle("Teste - Bloco Display IHM")
    window.setGeometry(100, 100, 400, 600)
    
    # Widget central
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # Biblioteca de componentes
    library = ComponentLibrary()
    layout.addWidget(library)
    
    window.setCentralWidget(central)
    window.show()
    
    print("✅ Teste do Bloco Display IHM iniciado")
    print("🖥️ Procure pelo grupo 'Interface IHM' na biblioteca")
    print("👆 Clique no bloco 'Display IHM' para testar")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_display_ihm()
#!/usr/bin/env python3
"""
Teste Direto - Bloco Display IHM
Teste isolado do componente DisplayIHMComponent
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def test_display_component():
    """Testa diretamente o componente Display IHM"""
    
    app = QApplication(sys.argv)
    
    # Janela de teste
    window = QMainWindow()
    window.setWindowTitle("✅ Teste Direto - Display IHM")
    window.setGeometry(100, 100, 600, 400)
    
    # Widget central
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # Título
    title = QLabel("🧪 Teste Componente Display IHM")
    title.setFont(QFont("Arial", 16, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("""
        QLabel {
            color: #2d5aa0;
            background-color: #f0f8ff;
            padding: 15px;
            border: 2px solid #b8d4f0;
            border-radius: 8px;
            margin: 10px;
        }
    """)
    layout.addWidget(title)
    
    # Tentar importar e criar o componente
    try:
        from component_library import DisplayIHMComponent
        
        # Criar componente Display IHM
        display_component = DisplayIHMComponent()
        
        # Conectar sinal de clique
        display_component.configure_ihm.connect(lambda: print("🖥️ Clique no Display IHM detectado!"))
        
        # Adicionar ao layout
        layout.addWidget(display_component)
        
        # Status
        status = QLabel("✅ Componente Display IHM carregado com sucesso!\n\n👆 Clique no componente acima para testar")
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("""
            QLabel {
                color: #155724;
                background-color: #d4edda;
                padding: 10px;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                margin: 10px;
            }
        """)
        layout.addWidget(status)
        
    except Exception as e:
        # Erro na importação
        error_msg = QLabel(f"❌ Erro ao carregar componente:\n\n{str(e)}")
        error_msg.setAlignment(Qt.AlignCenter)
        error_msg.setStyleSheet("""
            QLabel {
                color: #721c24;
                background-color: #f8d7da;
                padding: 15px;
                border: 2px solid #f5c6cb;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        layout.addWidget(error_msg)
    
    layout.addStretch()
    window.setCentralWidget(central)
    window.show()
    
    print("🧪 Teste do componente Display IHM iniciado")
    print("📋 Verifique se o componente aparece e responde ao clique")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_display_component()
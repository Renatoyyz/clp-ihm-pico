#!/usr/bin/env python3
"""
CLP-IHM-PICO - Interface LADDER
Aplicação principal para programação visual de Raspberry Pi Pico
"""

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

def main():
    """Função principal da aplicação"""
    app = QApplication(sys.argv)
    
    # Criar janela principal
    window = MainWindow()
    window.show()
    
    # Executar aplicação
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
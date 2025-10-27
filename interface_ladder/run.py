#!/usr/bin/env python3
"""
Script de inicialização da Interface LADDER
Verifica dependências e executa a aplicação
"""

import sys
import os

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    # Verificar PyQt5
    try:
        import PyQt5.QtWidgets
        print("✅ PyQt5: OK")
    except ImportError:
        print("❌ PyQt5 não encontrado!")
        print("   Execute: pip install PyQt5")
        return False
    
    # Verificar pyserial
    try:
        import serial
        import serial.tools.list_ports
        print("✅ pyserial: OK")
    except ImportError:
        print("⚠️  pyserial não encontrado - funcionará em modo simulação")
        print("   Para funcionalidade completa: pip install pyserial")
    
    return True

def main():
    """Função principal"""
    print("🚀 CLP-IHM-PICO - Interface LADDER")
    print("=" * 50)
    
    if not check_dependencies():
        print("\n❌ Dependências faltando. Instale-as antes de continuar.")
        sys.exit(1)
    
    print("\n🎯 Iniciando aplicação...")
    
    # Importar e executar aplicação principal
    try:
        from main_window import main as run_app
        run_app()
    except ImportError as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
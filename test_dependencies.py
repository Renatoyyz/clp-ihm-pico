#!/usr/bin/env python3
"""
Teste de dependências - PyQt5 e pyserial
"""

def test_pyserial():
    """Testa se pyserial está funcionando"""
    try:
        import serial
        import serial.tools.list_ports
        print("✅ pyserial: OK")
        
        # Listar portas reais
        ports = list(serial.tools.list_ports.comports())
        print(f"📡 Encontradas {len(ports)} portas:")
        for port in ports:
            print(f"   - {port.device}: {port.description}")
        return True
    except ImportError as e:
        print(f"❌ pyserial: {e}")
        return False

def test_pyqt5():
    """Testa se PyQt5 está funcionando"""
    try:
        import PyQt5.QtWidgets as QtWidgets
        import PyQt5.QtCore as QtCore
        print("✅ PyQt5: OK")
        
        # Criar uma aplicação simples
        app = QtWidgets.QApplication([])
        
        # Criar janela de teste
        window = QtWidgets.QWidget()
        window.setWindowTitle("Teste PyQt5 - CLP-IHM-Pico")
        window.setGeometry(100, 100, 300, 200)
        
        layout = QtWidgets.QVBoxLayout()
        
        label = QtWidgets.QLabel("🎉 PyQt5 funcionando!")
        button = QtWidgets.QPushButton("Fechar")
        button.clicked.connect(window.close)
        
        layout.addWidget(label)
        layout.addWidget(button)
        window.setLayout(layout)
        
        window.show()
        print("🖥️  Janela PyQt5 criada com sucesso!")
        print("   Clique no botão 'Fechar' para continuar...")
        
        # Rodar a aplicação
        app.exec_()
        return True
        
    except ImportError as e:
        print(f"❌ PyQt5: {e}")
        return False
    except Exception as e:
        print(f"❌ PyQt5 erro: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 TESTE DE DEPENDÊNCIAS - CLP-IHM-PICO")
    print("=" * 60)
    
    # Teste pyserial
    print("\n1️⃣  Testando pyserial...")
    pyserial_ok = test_pyserial()
    
    # Teste PyQt5
    print("\n2️⃣  Testando PyQt5...")
    pyqt5_ok = test_pyqt5()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO DOS TESTES:")
    print(f"   pyserial: {'✅ OK' if pyserial_ok else '❌ FALHOU'}")
    print(f"   PyQt5:    {'✅ OK' if pyqt5_ok else '❌ FALHOU'}")
    
    if pyserial_ok and pyqt5_ok:
        print("\n🎉 TODAS AS DEPENDÊNCIAS ESTÃO FUNCIONANDO!")
        print("   Pronto para desenvolver a interface PyQt5!")
    else:
        print("\n⚠️  ALGUMAS DEPENDÊNCIAS FALHARAM")
        print("   Verifique as mensagens de erro acima")
    print("=" * 60)

if __name__ == "__main__":
    main()
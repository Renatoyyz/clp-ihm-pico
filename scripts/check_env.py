#!/usr/bin/env python3
"""
check_env.py - Verifica ambiente e dependências
Funciona com ou sem ambiente virtual
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header():
    """Imprime cabeçalho"""
    print("🔍 VERIFICAÇÃO DO AMBIENTE DE DESENVOLVIMENTO")
    print("=" * 50)

def check_python():
    """Verifica instalação do Python"""
    print(f"🐍 Python: {sys.version}")
    print(f"📍 Localização: {sys.executable}")
    
    # Verifica se está em ambiente virtual
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print("🟢 Ambiente virtual ATIVO")
    else:
        print("🔴 Ambiente virtual NÃO ATIVO")
    
    return True

def check_ssl():
    """Verifica suporte SSL"""
    try:
        import ssl
        print("🟢 SSL/TLS: Disponível")
        return True
    except ImportError:
        print("🔴 SSL/TLS: Não disponível")
        return False

def check_dependencies():
    """Verifica dependências do projeto"""
    deps = {
        'pyserial': 'serial',
        'PyQt5': 'PyQt5'
    }
    
    available = {}
    
    for name, import_name in deps.items():
        try:
            __import__(import_name)
            print(f"🟢 {name}: Instalado")
            available[name] = True
        except ImportError:
            print(f"🔴 {name}: Não instalado")
            available[name] = False
    
    return available

def check_pico_connection():
    """Verifica se consegue detectar Pico"""
    try:
        import serial.tools.list_ports
        
        ports = list(serial.tools.list_ports.comports())
        print(f"🔌 Portas seriais encontradas: {len(ports)}")
        
        pico_ports = []
        for port in ports:
            if any(keyword in port.description.lower() for keyword in ['pico', 'usb serial']):
                pico_ports.append(port)
                print(f"   📱 {port.device} - {port.description}")
        
        if not pico_ports:
            print("   ⚠️  Nenhum Pico detectado automaticamente")
        
        return len(pico_ports) > 0
        
    except ImportError:
        print("🔴 Não é possível verificar portas (pyserial não disponível)")
        return False

def show_recommendations(ssl_ok, deps_available):
    """Mostra recomendações baseadas no ambiente"""
    print("\n" + "=" * 50)
    print("💡 RECOMENDAÇÕES")
    print("=" * 50)
    
    if not ssl_ok:
        print("⚠️  SSL não disponível:")
        print("   - Instale Python via Homebrew: brew install python")
        print("   - Ou use pyenv para gerenciar versões Python")
        print("   - Alternativa: use apenas terminal_uploader.py")
    
    if not deps_available.get('pyserial', False):
        print("📦 Para instalar pyserial:")
        if ssl_ok:
            print("   pip install pyserial")
        else:
            print("   - Baixe manualmente do PyPI")
            print("   - Ou instale Python com SSL funcionando")
    
    if not deps_available.get('PyQt5', False):
        print("🖥️  Para interface gráfica:")
        if ssl_ok:
            print("   pip install PyQt5")
        else:
            print("   - Use apenas a versão terminal")
            print("   - Instale Python com SSL para PyQt5")
    
    print("\n✅ SEMPRE FUNCIONA:")
    print("   python terminal_uploader.py")

def create_activation_scripts():
    """Cria scripts de ativação convenientes"""
    
    # Script para ativar ambiente
    activate_script = '''#!/bin/bash
# activate.sh - Ativa ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Ambiente virtual ativado"
    echo "Para desativar: deactivate"
else
    echo "❌ Ambiente virtual não encontrado"
    echo "Execute: python3 -m venv .venv"
fi
'''
    
    with open('activate.sh', 'w') as f:
        f.write(activate_script)
    
    os.chmod('activate.sh', 0o755)
    
    # Script Python para execução direta
    run_script = '''#!/usr/bin/env python3
"""run.py - Executa terminal_uploader com ambiente correto"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    # Verifica se existe ambiente virtual
    venv_path = Path('.venv')
    
    if venv_path.exists():
        # Usa Python do ambiente virtual
        python_exec = venv_path / 'bin' / 'python'
        if python_exec.exists():
            print("🟢 Usando ambiente virtual")
            subprocess.run([str(python_exec), 'terminal_uploader.py'])
        else:
            print("🔴 Ambiente virtual corrompido, usando Python padrão")
            subprocess.run([sys.executable, 'terminal_uploader.py'])
    else:
        print("🟡 Usando Python padrão (ambiente virtual não encontrado)")
        subprocess.run([sys.executable, 'terminal_uploader.py'])

if __name__ == "__main__":
    main()
'''
    
    with open('run.py', 'w') as f:
        f.write(run_script)
    
    os.chmod('run.py', 0o755)
    
    print("📝 Scripts criados:")
    print("   ./activate.sh  - Ativa ambiente virtual")
    print("   ./run.py       - Executa terminal_uploader")

def main():
    """Função principal"""
    print_header()
    
    # Verificações
    python_ok = check_python()
    ssl_ok = check_ssl()
    deps_available = check_dependencies()
    pico_detected = check_pico_connection()
    
    # Criar scripts úteis
    create_activation_scripts()
    
    # Mostrar recomendações
    show_recommendations(ssl_ok, deps_available)
    
    print(f"\n🎯 RESUMO:")
    print(f"   Python: {'✅' if python_ok else '❌'}")
    print(f"   SSL/TLS: {'✅' if ssl_ok else '❌'}")
    print(f"   pyserial: {'✅' if deps_available.get('pyserial') else '❌'}")
    print(f"   PyQt5: {'✅' if deps_available.get('PyQt5') else '❌'}")
    print(f"   Pico detectado: {'✅' if pico_detected else '❌'}")
    
    # Determinar melhor aplicação para usar
    if deps_available.get('PyQt5') and deps_available.get('pyserial'):
        print("\n🏆 RECOMENDADO: python simple_pico_uploader.py")
    elif deps_available.get('pyserial'):
        print("\n🏆 RECOMENDADO: python terminal_uploader.py")
    else:
        print("\n🏆 RECOMENDADO: python terminal_uploader.py (modo limitado)")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
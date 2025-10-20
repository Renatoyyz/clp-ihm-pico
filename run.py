#!/usr/bin/env python3
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

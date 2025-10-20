"""
main.py - Arquivo principal do Pico
Executado automaticamente na inicialização
"""

print("=== RASPBERRY PI PICO ===")
print("Sistema iniciado!")
print("Arquivos disponíveis para execução:")

import os
files = os.listdir()
py_files = [f for f in files if f.endswith('.py') and f != 'main.py']

for i, f in enumerate(py_files, 1):
    print(f"{i}. {f}")

print("\nUse exec(open('arquivo.py').read()) para executar")
print("Exemplo: exec(open('blink_led.py').read())")

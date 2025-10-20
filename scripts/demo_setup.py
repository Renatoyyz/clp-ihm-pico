#!/usr/bin/env python3
"""
Demo e Teste Rápido do Pico Uploader
Cria arquivos de exemplo e testa funcionalidades
"""

import os
import sys
from pathlib import Path

# Tentar importar pyserial para verificação de portas
try:
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

def create_test_files():
    """Cria arquivos de exemplo para testar o upload"""
    
    # Código de exemplo 1: Blink LED
    blink_code = '''"""
Exemplo 1: Piscar LED onboard do Pico
"""
from machine import Pin
import time

led = Pin("LED", Pin.OUT)

print("LED piscando... (Ctrl+C para parar)")

try:
    while True:
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
except KeyboardInterrupt:
    led.off()
    print("LED parado")
'''
    
    # Código de exemplo 2: Leitura de botão
    button_code = '''"""
Exemplo 2: Leitura de botão com LED
Conecte um botão no GP2 (com pull-up interno)
"""
from machine import Pin
import time

button = Pin(2, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

print("Sistema botão/LED iniciado...")

try:
    while True:
        if not button.value():  # Botão pressionado (pull-up invertido)
            led.on()
            print("Botão pressionado!")
        else:
            led.off()
        time.sleep(0.1)
except KeyboardInterrupt:
    led.off()
    print("Sistema parado")
'''
    
    # Código de exemplo 3: Sistema LADDER básico
    ladder_code = '''"""
Exemplo 3: Sistema LADDER Básico
"""
from machine import Pin
import time

# Entradas
input1 = Pin(2, Pin.IN, Pin.PULL_UP)
input2 = Pin(3, Pin.IN, Pin.PULL_UP)

# Saídas  
output1 = Pin(18, Pin.OUT)
led_onboard = Pin("LED", Pin.OUT)

# Variável auxiliar
memory1 = False

def ladder_scan():
    """Um ciclo de scan da lógica LADDER"""
    global memory1
    
    # Lê entradas (invertido por causa do pull-up)
    i1 = not input1.value()
    i2 = not input2.value()
    
    # RUNG 1: Se I1 AND I2 então M1 = True
    memory1 = i1 and i2
    
    # RUNG 2: Se M1 então OUTPUT1 = True
    output1.value(memory1)
    
    # RUNG 3: LED onboard mostra status de M1
    led_onboard.value(memory1)
    
    return i1, i2, memory1

print("Sistema LADDER iniciado")
print("I1=GP2, I2=GP3, O1=GP18, LED=Onboard")

try:
    while True:
        i1, i2, m1 = ladder_scan()
        
        # Debug a cada segundo
        if time.ticks_ms() % 1000 < 100:
            print(f"I1:{i1} I2:{i2} M1:{m1}")
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    output1.off()
    led_onboard.off()
    print("Sistema LADDER parado")
'''
    
    # main.py - arquivo principal
    main_code = '''"""
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

print("\\nUse exec(open('arquivo.py').read()) para executar")
print("Exemplo: exec(open('blink_led.py').read())")
'''
    
    # boot.py - configuração de boot
    boot_code = '''"""
boot.py - Configuração de inicialização
Executado antes do main.py
"""

print("Configurando sistema...")

# Configurações podem ser adicionadas aqui
# Exemplo: configuração de WiFi, I2C, SPI, etc.

print("Sistema configurado!")
'''
    
    # Cria os arquivos
    test_files = {
        'blink_led.py': blink_code,
        'button_led.py': button_code,
        'ladder_basic.py': ladder_code,
        'main.py': main_code,
        'boot.py': boot_code
    }
    
    examples_dir = Path('examples')
    examples_dir.mkdir(exist_ok=True)
    
    created_files = []
    for filename, content in test_files.items():
        filepath = examples_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        created_files.append(str(filepath))
        print(f"✅ Criado: {filepath}")
    
    return created_files

def show_usage_examples():
    """Mostra exemplos de uso"""
    print("\n" + "="*60)
    print("🚀 COMO USAR O PICO UPLOADER")
    print("="*60)
    
    print("\n1️⃣ EXECUTAR A APLICAÇÃO:")
    print("   python3 terminal_uploader.py")
    
    print("\n2️⃣ CONECTAR AO PICO:")
    print("   - Escolha opção 1 para listar portas")
    print("   - Escolha opção 2 para conectar")
    print("   - Selecione a porta do seu Pico")
    
    print("\n3️⃣ FAZER UPLOAD:")
    print("   - Opção 3: Upload arquivo único")
    print("   - Opção 4: Upload pasta inteira")
    print("   - Use os arquivos de exemplo criados em examples/")
    
    print("\n4️⃣ TESTAR NO PICO:")
    print("   - Opção 6: Executar main.py")
    print("   - Opção 8: Comando personalizado")
    print("   - Exemplo: exec(open('blink_led.py').read())")
    
    print("\n🔧 COMANDOS ÚTEIS NO PICO:")
    print("   import os; os.listdir()     # Lista arquivos")
    print("   import machine; machine.freq()  # Mostra frequência")
    print("   import sys; sys.version     # Versão MicroPython")
    print("   help()                      # Ajuda do MicroPython")

def check_pico_connection():
    """Verifica se há dispositivos que podem ser Pico"""
    if not SERIAL_AVAILABLE:
        print("\n⚠️  pyserial não instalado - não é possível verificar portas")
        return
    
    try:
        potential_picos = []
        for port in serial.tools.list_ports.comports():
            description = port.description.lower()
            if any(keyword in description for keyword in ['pico', 'usb serial', 'micropython']):
                potential_picos.append(port)
        
        if potential_picos:
            print(f"\n🔍 POSSÍVEIS DISPOSITIVOS PICO ENCONTRADOS ({len(potential_picos)}):")
            for port in potential_picos:
                print(f"   📱 {port.device} - {port.description}")
        else:
            print("\n⚠️  NENHUM PICO ÓBVIO ENCONTRADO")
            print("Verifique se:")
            print("   - Pico está conectado via USB")
            print("   - MicroPython está instalado no Pico")
            print("   - Drivers USB estão funcionando")
        
    except Exception as e:
        print(f"\n⚠️  Erro ao verificar portas: {e}")

def main():
    """Função principal do demo"""
    print("🥧 RASPBERRY PI PICO UPLOADER - SETUP E DEMO")
    print("="*60)
    
    print("\n📁 CRIANDO ARQUIVOS DE EXEMPLO...")
    created_files = create_test_files()
    
    print(f"\n✅ {len(created_files)} arquivos de exemplo criados!")
    
    check_pico_connection()
    
    show_usage_examples()
    
    print("\n" + "="*60)
    print("🎯 PRÓXIMOS PASSOS:")
    print("="*60)
    print("1. Execute: python3 terminal_uploader.py")
    print("2. Conecte ao seu Raspberry Pi Pico")
    print("3. Faça upload dos arquivos em examples/")
    print("4. Teste os exemplos no Pico")
    print("5. Desenvolva sua lógica LADDER!")
    
    print("\n💡 DICA: Comece com blink_led.py para testar a conexão")
    print("="*60)

if __name__ == "__main__":
    main()
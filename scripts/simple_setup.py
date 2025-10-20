#!/usr/bin/env python3
"""
Setup Simplificado - Funciona sem dependências
Cria arquivos de exemplo sem verificação de portas seriais
"""

import os
import sys
from pathlib import Path

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
Implementa lógica LADDER simples no Pico
"""
from machine import Pin
import time

# Configuração I/O
# Entradas (com pull-up interno)
input1 = Pin(2, Pin.IN, Pin.PULL_UP)   # Entrada 1 - GP2
input2 = Pin(3, Pin.IN, Pin.PULL_UP)   # Entrada 2 - GP3
sensor = Pin(4, Pin.IN, Pin.PULL_UP)   # Sensor - GP4

# Saídas  
output1 = Pin(18, Pin.OUT)      # Saída 1 - GP18
output2 = Pin(19, Pin.OUT)      # Saída 2 - GP19
relay = Pin(20, Pin.OUT)        # Relé - GP20
led_status = Pin("LED", Pin.OUT) # LED onboard

# Variáveis auxiliares (memórias)
memory1 = False
memory2 = False
timer_count = 0

def read_inputs():
    """Lê todas as entradas (inverte por causa do pull-up)"""
    return {
        'I1': not input1.value(),
        'I2': not input2.value(), 
        'SENSOR': not sensor.value()
    }

def ladder_logic(inputs):
    """
    Implementa a lógica LADDER
    
    RUNG 1: I1 AND I2 → M1
    RUNG 2: M1 OR SENSOR → O1  
    RUNG 3: I1 AND /I2 → Timer → O2
    RUNG 4: O1 → RELAY
    RUNG 5: M1 → LED_STATUS
    """
    global memory1, memory2, timer_count
    
    # RUNG 1: Lógica AND
    memory1 = inputs['I1'] and inputs['I2']
    
    # RUNG 2: Lógica OR
    output1_state = memory1 or inputs['SENSOR']
    output1.value(output1_state)
    
    # RUNG 3: Timer ON Delay (1 segundo)
    if inputs['I1'] and not inputs['I2']:
        timer_count += 1
        if timer_count >= 10:  # 10 ciclos * 0.1s = 1s
            output2.on()
    else:
        timer_count = 0
        output2.off()
    
    # RUNG 4: Controle de relé
    relay.value(output1_state)
    
    # RUNG 5: LED de status
    led_status.value(memory1)
    
    return {
        'O1': output1_state,
        'O2': output2.value(),
        'RELAY': relay.value(),
        'M1': memory1,
        'TIMER': timer_count
    }

def display_status(inputs, outputs):
    """Exibe status do sistema"""
    print("=" * 40)
    print("ENTRADAS | MEMÓRIAS | SAÍDAS")
    print("-" * 40)
    print(f"I1: {'ON ' if inputs['I1'] else 'OFF'} | M1: {'ON ' if outputs['M1'] else 'OFF'} | O1: {'ON ' if outputs['O1'] else 'OFF'}")
    print(f"I2: {'ON ' if inputs['I2'] else 'OFF'} | T1: {outputs['TIMER']:2d}  | O2: {'ON ' if outputs['O2'] else 'OFF'}")
    print(f"S1: {'ON ' if inputs['SENSOR'] else 'OFF'} |      |    | RL: {'ON ' if outputs['RELAY'] else 'OFF'}")
    print("=" * 40)

print("Sistema LADDER iniciado")
print("Conexões:")
print("- I1: GP2 (botão/chave)")
print("- I2: GP3 (botão/chave)")  
print("- SENSOR: GP4 (sensor)")
print("- O1: GP18 (LED/saída)")
print("- O2: GP19 (LED/saída)")
print("- RELAY: GP20 (relé)")
print("- STATUS: LED onboard")

cycle_count = 0

try:
    while True:
        # Ciclo de scan LADDER
        inputs = read_inputs()
        outputs = ladder_logic(inputs)
        
        # Mostra status a cada 2 segundos
        cycle_count += 1
        if cycle_count >= 20:  # 20 * 0.1s = 2s
            display_status(inputs, outputs)
            cycle_count = 0
        
        time.sleep(0.1)  # Ciclo de 100ms
        
except KeyboardInterrupt:
    # Desliga todas as saídas com segurança
    output1.off()
    output2.off()
    relay.off()
    led_status.off()
    print("\\nSistema LADDER parado com segurança")
'''
    
    # main.py melhorado
    main_code = '''"""
main.py - Sistema de Menu para Raspberry Pi Pico
Executado automaticamente na inicialização
"""

print("\\n" + "=" * 40)
print("🥧 RASPBERRY PI PICO - SISTEMA LADDER")
print("=" * 40)

import os
import time
import machine

print(f"Frequência: {machine.freq() // 1000000} MHz")
print(f"Memória livre: {machine.mem_free()} bytes")

# Lista arquivos disponíveis
print("\\n📄 ARQUIVOS DISPONÍVEIS:")
files = os.listdir()
py_files = [f for f in files if f.endswith('.py') and f != 'main.py']

if py_files:
    for i, f in enumerate(py_files, 1):
        size = 0
        try:
            with open(f, 'r') as file:
                size = len(file.read())
        except:
            pass
        print(f"  {i}. {f} ({size} bytes)")
else:
    print("  Nenhum arquivo Python encontrado")

print("\\n🔧 COMANDOS ÚTEIS:")
print("  exec(open('blink_led.py').read())      # Executa blink")
print("  exec(open('ladder_basic.py').read())   # Executa LADDER") 
print("  import os; os.listdir()               # Lista arquivos")
print("  machine.reset()                       # Reset do Pico")

print("\\n⚡ SISTEMA PRONTO!")
print("=" * 40)
'''
    
    # boot.py com configurações úteis
    boot_code = '''"""
boot.py - Configuração de inicialização
Executado antes do main.py
"""

import machine
import time

print("🔧 Configurando Raspberry Pi Pico...")

# Configuração de frequência (opcional)
# machine.freq(125000000)  # 125 MHz (padrão)

# Configuração de garbage collection
import gc
gc.enable()

# Informações do sistema
print(f"Versão MicroPython: {machine.uname()}")
print(f"Frequência CPU: {machine.freq() // 1000000} MHz")

# Configurações de rede (para Pico W)
try:
    import network
    print("Pico W detectado - WiFi disponível")
    # wlan = network.WLAN(network.STA_IF)
    # Configuração de WiFi pode ser adicionada aqui
except ImportError:
    print("Pico padrão - sem WiFi")

print("✅ Sistema configurado!")
time.sleep(1)  # Pequena pausa antes do main.py
'''

    # Arquivo de configuração LADDER
    ladder_config = '''"""
ladder_config.py - Configuração do Sistema LADDER
Define mapeamento de I/O e parâmetros do sistema
"""

# Mapeamento de I/O
IO_MAP = {
    # Entradas digitais
    'INPUTS': {
        'I1': {'pin': 2, 'description': 'Botão START'},
        'I2': {'pin': 3, 'description': 'Botão STOP'},
        'I3': {'pin': 4, 'description': 'Sensor de Posição'},
        'I4': {'pin': 5, 'description': 'Chave Limite'}
    },
    
    # Saídas digitais  
    'OUTPUTS': {
        'O1': {'pin': 18, 'description': 'Motor Principal'},
        'O2': {'pin': 19, 'description': 'Válvula 1'},
        'O3': {'pin': 20, 'description': 'Relé Auxiliar'},
        'O4': {'pin': 21, 'description': 'Alarme'}
    },
    
    # LEDs de status
    'STATUS_LEDS': {
        'RUN': 'LED',  # LED onboard
        'ERROR': 22
    }
}

# Parâmetros do sistema
SYSTEM_CONFIG = {
    'SCAN_TIME': 0.1,      # Tempo de ciclo em segundos
    'TIMER_RESOLUTION': 0.1, # Resolução dos timers
    'MAX_TIMERS': 10,       # Número máximo de timers
    'MAX_COUNTERS': 10,     # Número máximo de contadores
}

# Valores padrão dos timers (em segundos)
TIMER_PRESETS = {
    'T1': 1.0,    # Timer 1 - 1 segundo
    'T2': 5.0,    # Timer 2 - 5 segundos  
    'T3': 10.0,   # Timer 3 - 10 segundos
    'T4': 30.0,   # Timer 4 - 30 segundos
}

# Valores padrão dos contadores
COUNTER_PRESETS = {
    'C1': 10,     # Contador 1 - 10 pulsos
    'C2': 50,     # Contador 2 - 50 pulsos
    'C3': 100,    # Contador 3 - 100 pulsos
}

def get_pin_description(pin_type, pin_name):
    """Retorna descrição de um pino"""
    return IO_MAP.get(pin_type, {}).get(pin_name, {}).get('description', 'N/A')

def list_io_configuration():
    """Lista configuração completa de I/O"""
    print("CONFIGURAÇÃO DE I/O:")
    print("-" * 30)
    
    print("ENTRADAS:")
    for name, config in IO_MAP['INPUTS'].items():
        print(f"  {name}: GP{config['pin']} - {config['description']}")
    
    print("\\nSAÍDAS:")
    for name, config in IO_MAP['OUTPUTS'].items():
        print(f"  {name}: GP{config['pin']} - {config['description']}")
    
    print("\\nTIMERS:")
    for name, preset in TIMER_PRESETS.items():
        print(f"  {name}: {preset}s")

if __name__ == "__main__":
    list_io_configuration()
'''
    
    # Cria os arquivos
    test_files = {
        'blink_led.py': blink_code,
        'button_led.py': button_code,
        'ladder_basic.py': ladder_code,
        'main.py': main_code,
        'boot.py': boot_code,
        'ladder_config.py': ladder_config
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

def main():
    """Função principal simplificada"""
    print("🥧 RASPBERRY PI PICO - SETUP SIMPLIFICADO")
    print("=" * 50)
    
    print("\\n📁 CRIANDO ARQUIVOS DE EXEMPLO...")
    created_files = create_test_files()
    
    print(f"\\n✅ {len(created_files)} arquivos criados com sucesso!")
    
    print("\\n" + "=" * 50)
    print("🚀 PRÓXIMOS PASSOS:")
    print("=" * 50)
    print("1. Execute: python3 terminal_uploader.py")
    print("2. Conecte ao Raspberry Pi Pico")
    print("3. Faça upload dos arquivos da pasta examples/")
    print("4. Teste: exec(open('blink_led.py').read())")
    print("5. Execute: exec(open('ladder_basic.py').read())")
    
    print("\\n💡 DICAS:")
    print("- Comece com blink_led.py para testar")
    print("- Use ladder_basic.py para lógica LADDER")
    print("- Consulte ladder_config.py para I/O")
    
    print("\\n🎯 Agora você tem tudo para começar!")
    print("=" * 50)

if __name__ == "__main__":
    main()
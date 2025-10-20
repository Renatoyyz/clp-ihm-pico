"""
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
    
    print("\nSAÍDAS:")
    for name, config in IO_MAP['OUTPUTS'].items():
        print(f"  {name}: GP{config['pin']} - {config['description']}")
    
    print("\nTIMERS:")
    for name, preset in TIMER_PRESETS.items():
        print(f"  {name}: {preset}s")

if __name__ == "__main__":
    list_io_configuration()

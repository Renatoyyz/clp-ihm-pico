"""
Exemplo de Código LADDER Básico para Raspberry Pi Pico
Demonstra como a lógica LADDER pode ser implementada em MicroPython
"""

from machine import Pin
import time

# Configuração dos pinos I/O
# Entradas (inputs)
INPUT_1 = Pin(2, Pin.IN, Pin.PULL_UP)   # Botão 1
INPUT_2 = Pin(3, Pin.IN, Pin.PULL_UP)   # Botão 2
INPUT_3 = Pin(4, Pin.IN, Pin.PULL_UP)   # Sensor

# Saídas (outputs)
OUTPUT_1 = Pin(18, Pin.OUT)  # LED 1
OUTPUT_2 = Pin(19, Pin.OUT)  # LED 2
RELAY_1 = Pin(20, Pin.OUT)   # Relé 1

# Variáveis internas (memórias)
M1 = False  # Memória auxiliar 1
M2 = False  # Memória auxiliar 2
timer_1 = 0  # Timer 1

def read_inputs():
    """Lê o estado das entradas"""
    # Nota: Pull-up invertido (0 = pressionado, 1 = solto)
    i1 = not INPUT_1.value()
    i2 = not INPUT_2.value()
    i3 = not INPUT_3.value()
    return i1, i2, i3

def ladder_logic():
    """
    Implementa a lógica LADDER
    
    RUNG 1: Se INPUT_1 AND INPUT_2 então M1 = True
    RUNG 2: Se M1 OR INPUT_3 então OUTPUT_1 = True
    RUNG 3: Se INPUT_1 AND NOT INPUT_2 então OUTPUT_2 = True com timer
    RUNG 4: Se OUTPUT_1 então RELAY_1 = True
    """
    global M1, M2, timer_1
    
    # Lê entradas
    i1, i2, i3 = read_inputs()
    
    # RUNG 1: Lógica AND básica
    # ---|I1|---|I2|---( M1 )
    M1 = i1 and i2
    
    # RUNG 2: Lógica OR com memória
    # ---|M1|---+
    #           |---( O1 )
    # ---|I3|---+
    OUTPUT_1.value(M1 or i3)
    
    # RUNG 3: Lógica com NOT e timer
    # ---|I1|---|/I2|---[TON T1:1s]---( O2 )
    if i1 and not i2:
        timer_1 += 1
        if timer_1 >= 10:  # 10 ciclos = ~1 segundo
            OUTPUT_2.on()
    else:
        timer_1 = 0
        OUTPUT_2.off()
    
    # RUNG 4: Saída para relé
    # ---|O1|---( R1 )
    RELAY_1.value(OUTPUT_1.value())

def ladder_diagram_ascii():
    """
    Representação ASCII do diagrama LADDER
    """
    return """
    LADDER DIAGRAM - Exemplo Básico
    
    RUNG 1: Comando AND
    ---|I1|---|I2|---( M1 )
    
    RUNG 2: Comando OR 
    ---|M1|---+
              |---( O1 )
    ---|I3|---+
    
    RUNG 3: Timer ON Delay
    ---|I1|---|/I2|---[TON T1:1s]---( O2 )
    
    RUNG 4: Saída para Relé
    ---|O1|---( R1 )
    
    LEGENDA:
    I1, I2, I3 = Entradas (Inputs)
    O1, O2 = Saídas (Outputs)  
    M1 = Memória auxiliar
    R1 = Relé
    /I2 = Contato normalmente fechado
    TON = Timer ON Delay
    """

def status_display():
    """Exibe status atual do sistema"""
    i1, i2, i3 = read_inputs()
    
    print("\n" + "="*50)
    print("STATUS DO SISTEMA LADDER")
    print("="*50)
    print(f"ENTRADAS:")
    print(f"  INPUT_1 (I1): {'ON ' if i1 else 'OFF'}")
    print(f"  INPUT_2 (I2): {'ON ' if i2 else 'OFF'}")
    print(f"  INPUT_3 (I3): {'ON ' if i3 else 'OFF'}")
    print(f"\nMEMÓRIAS:")
    print(f"  M1: {'ON ' if M1 else 'OFF'}")
    print(f"  Timer_1: {timer_1}")
    print(f"\nSAÍDAS:")
    print(f"  OUTPUT_1 (O1): {'ON ' if OUTPUT_1.value() else 'OFF'}")
    print(f"  OUTPUT_2 (O2): {'ON ' if OUTPUT_2.value() else 'OFF'}")
    print(f"  RELAY_1 (R1):  {'ON ' if RELAY_1.value() else 'OFF'}")
    print("="*50)

def main():
    """Função principal - ciclo de execução LADDER"""
    print("Iniciando Sistema LADDER para Raspberry Pi Pico")
    print(ladder_diagram_ascii())
    
    print("\nSistema rodando... (Ctrl+C para parar)")
    
    cycle_count = 0
    
    try:
        while True:
            # Executa lógica LADDER
            ladder_logic()
            
            # Exibe status a cada 50 ciclos (~5 segundos)
            cycle_count += 1
            if cycle_count >= 50:
                status_display()
                cycle_count = 0
            
            # Tempo de ciclo: 100ms (10 Hz)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nSistema LADDER parado pelo usuário")
        # Desliga todas as saídas
        OUTPUT_1.off()
        OUTPUT_2.off()
        RELAY_1.off()
        print("Todas as saídas desligadas. Sistema seguro.")

if __name__ == "__main__":
    main()
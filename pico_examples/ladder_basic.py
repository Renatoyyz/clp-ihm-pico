"""
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

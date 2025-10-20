"""
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

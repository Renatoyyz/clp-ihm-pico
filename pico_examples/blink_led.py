"""
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

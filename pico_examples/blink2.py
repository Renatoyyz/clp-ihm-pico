from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        pin.toggle()
        sleep(0.1) # sleep 0.1 seconds
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")

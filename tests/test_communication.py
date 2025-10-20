import serial
import time

# Conecta ao Pico
ser = serial.Serial('/dev/cu.usbmodem141301', 115200, timeout=1)
time.sleep(1)

print('🔗 Conectado ao Pico')

# Teste simples
print('\n📤 Testando comunicação básica...')
ser.reset_input_buffer()
ser.write(b'print("Hello from Pico!")\r\n')
time.sleep(0.5)

response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print(f'Resposta: {repr(response)}')

# Teste de listagem
print('\n📂 Listando arquivos...')
ser.reset_input_buffer()
ser.write(b'import os; print(os.listdir())\r\n')
time.sleep(0.5)

response2 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print(f'Arquivos: {repr(response2)}')

# Teste de criação de arquivo
print('\n📝 Testando criação de arquivo...')
ser.reset_input_buffer()
test_content = "print('Teste')"
cmd = f"with open('test.py', 'w') as f: f.write('{test_content}')\r\n"
ser.write(cmd.encode())
time.sleep(1)

response3 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print(f'Resposta criação: {repr(response3)}')

# Verifica se arquivo foi criado
print('\n🔍 Verificando se arquivo foi criado...')
ser.reset_input_buffer()
ser.write(b'import os; print("test.py" in os.listdir())\r\n')
time.sleep(0.5)

response4 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print(f'Verificação: {repr(response4)}')

ser.close()
print('\n✅ Teste concluído')
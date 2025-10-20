"""
Teste final de upload após REPL ativo
"""
import serial
import time

def main():
    try:
        print('🔗 Conectando ao Pico...')
        ser = serial.Serial('/dev/cu.usbmodem141301', 115200, timeout=2)
        time.sleep(1)
        
        # Inicializa REPL
        print('🔄 Inicializando REPL...')
        ser.write(b'\x03')  # Ctrl+C
        time.sleep(0.5)
        ser.write(b'\x04')  # Ctrl+D
        time.sleep(2)
        
        # Limpa buffer
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Init response: {repr(response[:100])}...')
        
        # Teste 1: Comando simples
        print('\n=== TESTE 1: Comando simples ===')
        ser.reset_input_buffer()
        ser.write(b'print("Hello!")\r\n')
        time.sleep(0.5)
        
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Response: {repr(response)}')
        
        # Teste 2: Lista arquivos atual
        print('\n=== TESTE 2: Lista arquivos atual ===')
        ser.reset_input_buffer()
        ser.write(b'import os; print(os.listdir())\r\n')
        time.sleep(0.5)
        
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Arquivos: {repr(response)}')
        
        # Teste 3: Criar arquivo simples
        print('\n=== TESTE 3: Criar arquivo simples ===')
        content = "print('teste')"
        cmd = f'with open("test.py", "w") as f: f.write({repr(content)})\r\n'
        
        print(f'📤 Comando: {cmd[:80]}...')
        ser.reset_input_buffer()
        ser.write(cmd.encode())
        time.sleep(1)
        
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Create response: {repr(response)}')
        
        # Teste 4: Verifica arquivo
        print('\n=== TESTE 4: Verifica arquivo ===')
        ser.reset_input_buffer()
        ser.write(b'import os; print("test.py" in os.listdir())\r\n')
        time.sleep(0.5)
        
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Verification: {repr(response)}')
        
        ser.close()
        print('\n✅ Teste completo!')
        
    except Exception as e:
        print(f'❌ Erro: {e}')

if __name__ == '__main__':
    main()
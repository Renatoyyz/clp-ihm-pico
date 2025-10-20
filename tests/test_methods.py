"""
Teste de upload com comandos quebrados em partes menores
"""
import serial
import time

def send_command(ser, command, wait_time=1.0):
    """Envia comando e aguarda resposta completa"""
    print(f"📤 Enviando: {command[:50]}...")
    ser.reset_input_buffer()
    ser.write((command + '\r\n').encode())
    time.sleep(wait_time)
    
    response = ""
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    
    print(f"📥 Resposta: {repr(response)}")
    return response

def main():
    try:
        print('🔗 Conectando ao Pico...')
        ser = serial.Serial('/dev/cu.usbmodem141301', 115200, timeout=2)
        time.sleep(1)
        
        # Inicializa REPL
        print('🔄 Inicializando REPL...')
        ser.write(b'\x03')
        time.sleep(0.5)
        ser.write(b'\x04')
        time.sleep(2)
        
        # Limpa buffer inicial
        if ser.in_waiting > 0:
            ser.read(ser.in_waiting)
        
        print('\n=== MÉTODO 1: Comando em uma linha ===')
        send_command(ser, 'f = open("test1.py", "w")')
        send_command(ser, 'f.write("print(\\"Arquivo 1\\")")')
        send_command(ser, 'f.close()')
        send_command(ser, 'import os; print("test1.py" in os.listdir())')
        
        print('\n=== MÉTODO 2: Comando exec ===')
        code = 'print("Arquivo 2")'
        exec_cmd = f'exec(compile({repr(code)}, "test2.py", "exec"))'
        send_command(ser, exec_cmd)
        
        print('\n=== MÉTODO 3: Criação multi-linha ===')
        send_command(ser, 'content = "print(\\"Arquivo 3\\")"')
        send_command(ser, 'with open("test3.py", "w") as f: f.write(content)')
        send_command(ser, 'import os; print("test3.py" in os.listdir())')
        
        print('\n=== LISTA FINAL ===')
        send_command(ser, 'import os; print(os.listdir())')
        
        ser.close()
        print('\n✅ Teste completo!')
        
    except Exception as e:
        print(f'❌ Erro: {e}')

if __name__ == '__main__':
    main()
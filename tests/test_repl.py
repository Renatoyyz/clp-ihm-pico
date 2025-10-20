"""
Teste para entrar no modo REPL do MicroPython
"""
import serial
import time

def main():
    try:
        print('🔗 Conectando ao Pico...')
        ser = serial.Serial('/dev/cu.usbmodem141301', 115200, timeout=2)
        time.sleep(1)
        
        print('🔄 Tentando entrar no modo REPL...')
        
        # Método 1: Ctrl+C para interromper programa atual
        print('📤 Enviando Ctrl+C...')
        ser.write(b'\x03')  # Ctrl+C
        time.sleep(0.5)
        
        # Método 2: Ctrl+D para soft reset
        print('📤 Enviando Ctrl+D (soft reset)...')
        ser.write(b'\x04')  # Ctrl+D
        time.sleep(2)
        
        # Lê resposta
        response = ""
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Resposta após reset: {repr(response)}')
        
        # Teste comando simples
        print('📤 Testando comando simples...')
        ser.write(b'print("REPL ativo!")\r\n')
        time.sleep(0.5)
        
        response2 = ""
        if ser.in_waiting > 0:
            response2 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f'📥 Resposta do teste: {repr(response2)}')
        
        # Verifica se temos prompt ">>>"
        if ">>>" in response or ">>>" in response2:
            print('✅ REPL ativo!')
        else:
            print('❌ REPL não detectado')
            
        ser.close()
        
    except Exception as e:
        print(f'❌ Erro: {e}')

if __name__ == '__main__':
    main()
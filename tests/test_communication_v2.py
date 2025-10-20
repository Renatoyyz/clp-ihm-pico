"""
Teste de comunicação melhorado com Raspberry Pi Pico
Usa o protocolo correto de MicroPython
"""
import serial
import time

def send_command(ser, command, wait_time=0.5):
    """Envia comando e aguarda resposta"""
    print(f"📤 Enviando: {command[:50]}...")
    ser.reset_input_buffer()
    
    # Envia comando com terminadores corretos
    ser.write((command + '\r\n').encode('utf-8'))
    time.sleep(wait_time)
    
    # Lê resposta
    response = ""
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    
    print(f"📥 Resposta: {repr(response)}")
    return response

def main():
    try:
        # Conecta ao Pico
        print('🔗 Conectando ao Pico...')
        ser = serial.Serial('/dev/cu.usbmodem141301', 115200, timeout=2)
        time.sleep(2)  # Tempo para estabilizar conexão
        
        # Limpa buffer inicial
        ser.reset_input_buffer()
        time.sleep(0.5)
        
        print('✅ Conectado!')
        
        # Teste 1: Comando simples
        print('\n=== TESTE 1: Comando simples ===')
        send_command(ser, 'print("Hello from Pico!")')
        
        # Teste 2: Lista arquivos
        print('\n=== TESTE 2: Listar arquivos ===')
        send_command(ser, 'import os; print(os.listdir())')
        
        # Teste 3: Criar arquivo pequeno
        print('\n=== TESTE 3: Criar arquivo pequeno ===')
        test_code = 'print("Arquivo de teste")'
        create_cmd = f'with open("test.py", "w") as f: f.write({repr(test_code)})'
        send_command(ser, create_cmd, 1.0)
        
        # Teste 4: Verificar se arquivo existe
        print('\n=== TESTE 4: Verificar arquivo ===')
        send_command(ser, 'import os; print("test.py" in os.listdir())')
        
        # Teste 5: Ler conteúdo do arquivo
        print('\n=== TESTE 5: Ler arquivo ===')
        send_command(ser, 'with open("test.py", "r") as f: print(repr(f.read()))')
        
        # Teste 6: Executar arquivo
        print('\n=== TESTE 6: Executar arquivo ===')
        send_command(ser, 'exec(open("test.py").read())')
        
        ser.close()
        print('\n✅ Testes concluídos!')
        
    except Exception as e:
        print(f'❌ Erro: {e}')

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Terminal Uploader - Versão que funciona SEM dependências
Interface de linha de comando para Raspberry Pi Pico
"""

import os
import sys
import time
import glob
from pathlib import Path

# Verificar se pyserial está disponível
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
    print("✅ pyserial disponível - funcionalidade completa")
except ImportError:
    SERIAL_AVAILABLE = False
    print("⚠️  pyserial não disponível - modo simulação")

class MockSerial:
    """Classe mock para simular pyserial quando não disponível"""
    
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = True
        print(f"🔧 SIMULAÇÃO: Conectado em {port} @ {baudrate}")
    
    def write(self, data):
        if isinstance(data, str):
            data = data.encode()
        print(f"📤 SIMULAÇÃO TX: {data.decode('utf-8', errors='ignore')}")
        return len(data)
    
    def read(self, size=1):
        # Simula resposta do Pico
        return b"OK\n"
    
    def close(self):
        self.is_open = False
        print("🔧 SIMULAÇÃO: Conexão fechada")
    
    def reset_input_buffer(self):
        print("🔧 SIMULAÇÃO: Buffer limpo")
    
    @property
    def in_waiting(self):
        return 3  # Simula que sempre há alguns bytes

class MockListPorts:
    """Mock para list_ports quando pyserial não disponível"""
    
    @staticmethod
    def comports():
        # Retorna portas simuladas típicas do macOS
        class MockPort:
            def __init__(self, device, description):
                self.device = device
                self.description = description
        
        return [
            MockPort("/dev/tty.usbmodem101", "USB Serial Device"),
            MockPort("/dev/tty.usbmodem102", "Raspberry Pi Pico"),
            MockPort("/dev/cu.BLTH", "Bluetooth Device")
        ]

# Usar versões mock se pyserial não disponível
if not SERIAL_AVAILABLE:
    serial = type('MockSerial', (), {'Serial': MockSerial})()
    serial.tools = type('tools', (), {'list_ports': MockListPorts})()

class PicoUploader:
    """Uploader para Raspberry Pi Pico"""
    
    def __init__(self):
        self.serial_conn = None
        self.connected = False
        self.current_port = None
        self.simulation_mode = not SERIAL_AVAILABLE
        
    def list_ports(self):
        """Lista portas seriais disponíveis"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'description': port.description
            })
        return ports
    
    def check_pico_mode(self, port_description):
        """Verifica o modo do Pico baseado na descrição da porta"""
        # BOOTSEL real aparece geralmente como "RP2 Boot" ou similares
        # "Board in FS mode" pode ser MicroPython normal
        if "RP2 Boot" in port_description or "Pico Boot" in port_description:
            return "BOOTSEL"
        elif "MicroPython" in port_description or "Board in FS mode" in port_description:
            return "MICROPYTHON"
        elif "USB Serial" in port_description:
            return "SERIAL"
        else:
            return "MICROPYTHON"  # Assume MicroPython por padrão para Pico
    
    def connect(self, port, baudrate=115200):
        """Conecta ao Pico"""
        # Primeiro verifica se a porta indica modo BOOTSEL
        port_info = None
        for p in self.list_ports():
            if p['device'] == port:
                port_info = p
                break
        
        if port_info:
            mode = self.check_pico_mode(port_info['description'])
            if mode == "BOOTSEL":
                print("⚠️  ATENÇÃO: Pico está no modo BOOTSEL (FS mode)")
                print("📋 Para usar upload via MicroPython:")
                print("   1. Desconecte o Pico do USB")
                print("   2. Reconecte SEM segurar o botão BOOTSEL")
                print("   3. O Pico deve aparecer como dispositivo serial normal")
                print("   4. Tente conectar novamente")
                return False
        
        try:
            self.serial_conn = serial.Serial(port, baudrate, timeout=1)
            time.sleep(0.1)
            
            if not self.simulation_mode:
                # Inicializa REPL do MicroPython corretamente
                print("🔄 Inicializando REPL...")
                self.serial_conn.write(b'\x03')  # Ctrl+C para parar programa atual
                time.sleep(0.5)
                self.serial_conn.write(b'\x04')  # Ctrl+D para soft reset
                time.sleep(2)  # Aguarda reboot
                
                # Verifica se REPL está ativo
                self.serial_conn.reset_input_buffer()
                self.serial_conn.write(b'print("PICO_TEST")\r\n')
                time.sleep(0.5)
                
                response = ""
                if self.serial_conn.in_waiting > 0:
                    response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                
                if "PICO_TEST" in response and ">>>" in response:
                    print("✅ REPL ativo e funcionando!")
                elif "PICO_TEST" in response:
                    print("✅ MicroPython respondendo!")
                else:
                    print("⚠️  AVISO: REPL pode não estar ativo")
                    print("� Verifique se MicroPython está instalado no Pico")
            
            self.connected = True
            self.current_port = port
            print(f"✅ Conectado em {port}! (REAL)")
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do Pico"""
        if self.serial_conn:
            self.serial_conn.close()
        self.connected = False
        self.current_port = None
    
    def upload_file(self, local_path, remote_name=None):
        """Faz upload de arquivo"""
        if not self.connected:
            print("❌ Não conectado ao Pico")
            return False
            
        if remote_name is None:
            remote_name = os.path.basename(local_path)
        
        try:
            # Lê arquivo local
            with open(local_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📤 Enviando {remote_name} ({len(content)} bytes)...")
            
            if self.simulation_mode:
                print(f"🔧 SIMULAÇÃO: Arquivo {remote_name} 'enviado' com sucesso")
                time.sleep(0.5)  # Simula tempo de upload
                return True
            
            # Método corrigido: upload em partes para evitar problemas de buffer
            # Passo 1: Abre arquivo para escrita
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(f'f = open("{remote_name}", "w")\r\n'.encode())
            time.sleep(0.5)
            
            response1 = ""
            if self.serial_conn.in_waiting > 0:
                response1 = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                print(f"📋 Abertura: {response1.strip()}")
            
            # Passo 2: Escreve conteúdo
            self.serial_conn.reset_input_buffer()
            write_cmd = f'f.write({repr(content)})\r\n'
            self.serial_conn.write(write_cmd.encode())
            time.sleep(1.0)  # Mais tempo para escrita
            
            response2 = ""
            if self.serial_conn.in_waiting > 0:
                response2 = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                print(f"📋 Escrita: {response2.strip()}")
            
            # Passo 3: Fecha arquivo
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(b'f.close()\r\n')
            time.sleep(0.5)
            
            response3 = ""
            if self.serial_conn.in_waiting > 0:
                response3 = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                print(f"📋 Fechamento: {response3.strip()}")
            
            # Verifica se houve erro em qualquer passo
            if any("Error" in resp or "Traceback" in resp for resp in [response1, response2, response3]):
                print(f"❌ Erro no upload detectado")
                return False
            
            # Verificação adicional: confirma se arquivo existe no Pico
            print(f"🔍 Verificando se {remote_name} foi criado...")
            self.serial_conn.reset_input_buffer()
            check_cmd = f'import os; print("{remote_name}" in os.listdir())\r\n'
            self.serial_conn.write(check_cmd.encode())
            time.sleep(0.5)
            
            verification = ""
            if self.serial_conn.in_waiting > 0:
                verification = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                print(f"📋 Verificação: {verification.strip()}")
            
            if "True" in verification:
                print(f"✅ {remote_name} enviado e verificado com sucesso!")
                return True
            else:
                print(f"❌ Arquivo não foi encontrado no Pico após upload")
                print(f"   Resposta da verificação: {verification}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return False
    
    def list_files(self):
        """Lista arquivos no Pico"""
        if not self.connected:
            return []
        
        if self.simulation_mode:
            # Retorna arquivos simulados
            return ["main.py", "blink_led.py", "boot.py"]
        
        try:
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(b"import os; print(os.listdir())\r\n")
            time.sleep(0.5)
            
            response = ""
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
            
            # Extrai lista de arquivos
            lines = response.split('\n')
            for line in lines:
                if '[' in line and ']' in line:
                    files_str = line.strip()
                    if files_str.startswith('[') and files_str.endswith(']'):
                        files_str = files_str[1:-1]
                        files = [f.strip().strip("'\"") for f in files_str.split(',') if f.strip()]
                        return files
            
            return []
            
        except Exception as e:
            print(f"❌ Erro ao listar arquivos: {e}")
            return []
    
    def run_command(self, command):
        """Executa comando no Pico"""
        if not self.connected:
            print("❌ Não conectado")
            return ""
        
        if self.simulation_mode:
            print(f"🔧 SIMULAÇÃO: Executando '{command}'")
            return f"SIMULAÇÃO: Comando '{command}' executado"
        
        try:
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(command.encode() + b'\r\n')
            time.sleep(0.5)
            
            response = ""
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
            
            return response
            
        except Exception as e:
            return f"Erro: {e}"

def print_header():
    """Imprime cabeçalho da aplicação"""
    print("="*60)
    print("🥧 RASPBERRY PI PICO FILE UPLOADER")
    if not SERIAL_AVAILABLE:
        print("🔧 MODO SIMULAÇÃO (pyserial não disponível)")
    print("="*60)
    print("Interface universal - funciona sempre!")
    print("Compatível com Pico, Pico W, Pico 2 e Pico 2W")
    print("="*60)

def print_menu():
    """Imprime menu principal"""
    print("\n📋 MENU PRINCIPAL")
    print("-" * 30)
    print("1. 🔍 Listar portas disponíveis")
    print("2. 🔌 Conectar ao Pico")
    print("3. 📤 Upload arquivo único")
    print("3R.🚀 Upload + Executar arquivo")
    print("4. 📁 Upload pasta (todos .py)")
    print("5. 📄 Listar arquivos do Pico")
    print("6. ▶️  Executar main.py")
    print("7. 🔄 Reset Pico")
    print("8. 💬 Comando personalizado")
    print("9. ❌ Desconectar")
    print("0. 🚪 Sair")
    if not SERIAL_AVAILABLE:
        print("⚠️  MODO SIMULAÇÃO ATIVO")
    print("-" * 30)

def main():
    """Função principal"""
    print_header()
    
    uploader = PicoUploader()
    
    # Mostra status de dependências
    if not SERIAL_AVAILABLE:
        print("\n💡 MODO SIMULAÇÃO:")
        print("   - pyserial não está instalado")
        print("   - Todas as operações são simuladas")
        print("   - Para funcionalidade completa: pip install pyserial")
        print("   - Ou configure ambiente virtual com SSL")
    
    while True:
        print_menu()
        
        if uploader.connected:
            mode = "SIMULAÇÃO" if uploader.simulation_mode else "REAL"
            print(f"🟢 Conectado em: {uploader.current_port} ({mode})")
        else:
            print("🔴 Desconectado")
        
        try:
            choice = input("\n👉 Escolha uma opção: ").strip()
            
            if choice == "0":
                print("👋 Saindo...")
                if uploader.connected:
                    uploader.disconnect()
                break
                
            elif choice == "1":
                print("\n🔍 PORTAS DISPONÍVEIS:")
                ports = uploader.list_ports()
                if ports:
                    bootsel_ports = []
                    micropython_ports = []
                    
                    for i, port in enumerate(ports, 1):
                        mode = uploader.check_pico_mode(port['description'])
                        if mode == "BOOTSEL":
                            print(f"   {i}. {port['device']} - {port['description']} ⚠️  [MODO BOOTSEL]")
                            bootsel_ports.append(port['device'])
                        else:
                            print(f"   {i}. {port['device']} - {port['description']}")
                            if "Pico" in port['description'] or "Board" in port['description']:
                                micropython_ports.append(port['device'])
                    
                    if uploader.simulation_mode:
                        print("   ⚠️  Portas simuladas (pyserial não disponível)")
                    
                    # Aviso refinado sobre modo BOOTSEL
                    if bootsel_ports:
                        print(f"\n⚠️  ATENÇÃO: Portas em MODO BOOTSEL detectadas: {', '.join(bootsel_ports)}")
                        print("💡 Para upload via MicroPython:")
                        print("   - Desconecte e reconecte o Pico SEM segurar BOOTSEL")
                        print("   - O Pico deve aparecer como porta serial normal")
                    elif micropython_ports:
                        print(f"\n✅ Portas Pico em modo MicroPython: {', '.join(micropython_ports)}")
                else:
                    print("   Nenhuma porta encontrada")
                
            elif choice == "2":
                ports = uploader.list_ports()
                if not ports:
                    print("❌ Nenhuma porta disponível")
                    continue
                
                print("\n🔍 PORTAS DISPONÍVEIS:")
                for i, port in enumerate(ports, 1):
                    print(f"   {i}. {port['device']} - {port['description']}")
                
                try:
                    port_num = int(input("Escolha uma porta (número): ")) - 1
                    if 0 <= port_num < len(ports):
                        port = ports[port_num]['device']
                        print(f"🔌 Conectando em {port}...")
                        if uploader.connect(port):
                            mode = "SIMULAÇÃO" if uploader.simulation_mode else "REAL"
                            print(f"✅ Conectado em {port}! ({mode})")
                        else:
                            print("❌ Falha na conexão")
                    else:
                        print("❌ Número inválido")
                except ValueError:
                    print("❌ Entrada inválida")
            
            elif choice == "3":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                file_path = input("📁 Caminho do arquivo .py: ").strip()
                if os.path.exists(file_path):
                    # Faz upload do arquivo
                    remote_name = os.path.basename(file_path)
                    if uploader.upload_file(file_path, remote_name):
                        # Pergunta se quer executar
                        execute = input(f"▶️  Executar {remote_name} agora? (s/N): ").strip().lower()
                        if execute in ['s', 'sim', 'y', 'yes']:
                            print(f"🚀 Executando {remote_name}...")
                            response = uploader.run_command(f"exec(open('{remote_name}').read())")
                            if response:
                                print("📄 Saída:")
                                print(response)
                        else:
                            print(f"💾 Arquivo {remote_name} salvo no Pico (use opção 6 para executar main.py)")
                else:
                    print("❌ Arquivo não encontrado")
            
            elif choice.upper() == "3R":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                file_path = input("📁 Caminho do arquivo .py: ").strip()
                if os.path.exists(file_path):
                    # Upload e execução automática
                    remote_name = os.path.basename(file_path)
                    print(f"📤 Enviando e executando {remote_name}...")
                    if uploader.upload_file(file_path, remote_name):
                        print(f"🚀 Executando {remote_name} automaticamente...")
                        response = uploader.run_command(f"exec(open('{remote_name}').read())")
                        if response:
                            print("📄 Saída:")
                            print(response)
                    else:
                        print("❌ Falha no upload - não foi possível executar")
                else:
                    print("❌ Arquivo não encontrado")
            
            elif choice == "4":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                folder_path = input("📁 Caminho da pasta: ").strip()
                if os.path.exists(folder_path):
                    py_files = list(Path(folder_path).glob("**/*.py"))
                    if py_files:
                        print(f"📤 Enviando {len(py_files)} arquivo(s)...")
                        success_count = 0
                        for file_path in py_files:
                            if uploader.upload_file(str(file_path)):
                                success_count += 1
                        print(f"✅ {success_count}/{len(py_files)} arquivos enviados")
                    else:
                        print("❌ Nenhum arquivo .py encontrado")
                else:
                    print("❌ Pasta não encontrada")
            
            elif choice == "5":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                files = uploader.list_files()
                print(f"\n📄 ARQUIVOS NO PICO ({len(files)}):")
                for file in files:
                    print(f"   - {file}")
                if uploader.simulation_mode:
                    print("   ⚠️  Lista simulada")
            
            elif choice == "6":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                print("▶️ Executando main.py...")
                response = uploader.run_command("exec(open('main.py').read())")
                if response:
                    print("📄 Saída:")
                    print(response)
            
            elif choice == "7":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                print("🔄 Resetando Pico...")
                try:
                    if uploader.simulation_mode:
                        print("🔧 SIMULAÇÃO: Reset do Pico simulado")
                        continue
                    
                    # Método 1: Soft reset (Ctrl+D) - mais suave
                    print("   📤 Enviando soft reset (Ctrl+D)...")
                    if uploader.serial_conn:
                        uploader.serial_conn.write(b'\x04')  # Ctrl+D
                        time.sleep(2)
                        
                        # Verifica se reconectou
                        response = ""
                        if uploader.serial_conn.in_waiting > 0:
                            response = uploader.serial_conn.read(uploader.serial_conn.in_waiting).decode('utf-8', errors='ignore')
                            print(f"📋 Resposta: {response[:100]}...")
                        
                        if "MicroPython" in response or ">>>" in response:
                            print("✅ Soft reset realizado com sucesso!")
                        else:
                            # Método 2: Hard reset via machine.reset()
                            print("   📤 Tentando hard reset...")
                            uploader.serial_conn.reset_input_buffer()
                            uploader.serial_conn.write(b'import machine; machine.reset()\r\n')
                            time.sleep(1)
                            
                            # Após hard reset, a conexão pode ser perdida
                            print("⚠️  Hard reset enviado - reconexão pode ser necessária")
                            uploader.connected = False
                            uploader.current_port = None
                    else:
                        print("❌ Conexão serial não disponível")
                        
                except Exception as e:
                    print(f"❌ Erro durante reset: {e}")
                    uploader.connected = False
                    uploader.current_port = None
            
            elif choice == "8":
                if not uploader.connected:
                    print("❌ Conecte ao Pico primeiro (opção 2)")
                    continue
                
                command = input("💻 Comando MicroPython: ").strip()
                if command:
                    response = uploader.run_command(command)
                    if response:
                        print("📄 Resposta:")
                        print(response)
            
            elif choice == "9":
                if uploader.connected:
                    uploader.disconnect()
                    print("✅ Desconectado")
                else:
                    print("❌ Não estava conectado")
            
            else:
                print("❌ Opção inválida")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            if uploader.connected:
                uploader.disconnect()
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
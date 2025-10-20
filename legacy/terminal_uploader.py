#!/usr/bin/env python3
"""
Raspberry Pi Pico File Uploader - Versão Terminal
Versão que funciona apenas no terminal, sem dependências gráficas
Ideal para quando PyQt5 não está disponível
"""

import os
import sys
import time
import glob
from pathlib import Path

# Tentar importar pyserial, se não estiver disponível, mostrar instruções
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("⚠️  pyserial não está disponível")

class TerminalPicoUploader:
    """Uploader para Pico usando interface de terminal"""
    
    def __init__(self):
        self.serial_conn = None
        self.connected = False
        self.current_port = None
        
    def list_ports(self):
        """Lista portas seriais disponíveis"""
        if not SERIAL_AVAILABLE:
            return []
            
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'description': port.description,
                'hwid': port.hwid
            })
        return ports
    
    def connect(self, port, baudrate=115200):
        """Conecta ao Pico"""
        if not SERIAL_AVAILABLE:
            print("❌ pyserial não está instalado")
            return False
            
        try:
            self.serial_conn = serial.Serial(port, baudrate, timeout=1)
            time.sleep(0.1)
            
            # Testa conexão
            self.serial_conn.write(b'\x03\r\n')  # Ctrl+C + Enter
            time.sleep(0.2)
            
            self.connected = True
            self.current_port = port
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
            with open(local_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📤 Enviando {remote_name}...")
            
            # Limpa buffer
            self.serial_conn.reset_input_buffer()
            
            # Comando para criar arquivo
            cmd = f"with open('{remote_name}', 'w') as f:\n    f.write({repr(content)})\n"
            
            self.serial_conn.write(cmd.encode() + b'\r\n')
            time.sleep(0.5)
            
            # Verifica resposta
            response = ""
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
            
            if "Error" not in response and "Traceback" not in response:
                print(f"✅ {remote_name} enviado com sucesso!")
                return True
            else:
                print(f"❌ Erro no upload: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return False
    
    def list_files(self):
        """Lista arquivos no Pico"""
        if not self.connected:
            return []
        
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
    print("🥧 RASPBERRY PI PICO FILE UPLOADER - Terminal Version")
    print("="*60)
    print("Interface de linha de comando para upload de arquivos")
    print("Compatível com Pico, Pico W, Pico 2 e Pico 2W")
    print("="*60)

def print_menu():
    """Imprime menu principal"""
    print("\n📋 MENU PRINCIPAL")
    print("-" * 30)
    print("1. 🔍 Listar portas disponíveis")
    print("2. 🔌 Conectar ao Pico")
    print("3. 📤 Upload arquivo único")
    print("4. 📁 Upload pasta (todos .py)")
    print("5. 📄 Listar arquivos do Pico")
    print("6. ▶️  Executar main.py")
    print("7. 🔄 Reset Pico")
    print("8. 💬 Comando personalizado")
    print("9. ❌ Desconectar")
    print("0. 🚪 Sair")
    print("-" * 30)

def check_dependencies():
    """Verifica se dependências estão instaladas"""
    issues = []
    
    if not SERIAL_AVAILABLE:
        issues.append("pyserial não está instalado")
    
    if issues:
        print("⚠️  DEPENDÊNCIAS FALTANDO:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n🔧 PARA INSTALAR:")
        print("   pip3 install pyserial")
        print("   ou")
        print("   python -m pip install pyserial")
        print("\n💡 ALTERNATIVAS:")
        print("   - Use conda: conda install pyserial")
        print("   - Use package manager do sistema")
        print("   - Instale manualmente do GitHub")
        return False
    
    return True

def main():
    """Função principal"""
    print_header()
    
    if not check_dependencies():
        print("\n❌ Não é possível continuar sem as dependências")
        print("Instale pyserial e execute novamente")
        return
    
    uploader = TerminalPicoUploader()
    
    while True:
        print_menu()
        
        if uploader.connected:
            print(f"🟢 Conectado em: {uploader.current_port}")
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
                    for i, port in enumerate(ports, 1):
                        print(f"   {i}. {port['device']} - {port['description']}")
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
                            print(f"✅ Conectado em {port}!")
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
                    uploader.upload_file(file_path)
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
                        for file_path in py_files:
                            uploader.upload_file(str(file_path))
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
                uploader.run_command("import machine; machine.reset()")
                print("✅ Comando de reset enviado")
            
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
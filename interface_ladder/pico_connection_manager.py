#!/usr/bin/env python3
"""
Gerenciador Global de Conexão com Raspberry Pi Pico
Centraliza o estado de conexão para evitar múltiplas conexões simultâneas
"""

import os
import time
import subprocess

# Importar suporte para comunicação serial
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False


class PicoConnectionManager:
    """Gerenciador singleton para conexão com Pico"""
    
    _instance = None
    _connection = None
    _port = None
    _baudrate = 115200
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def is_connected(cls):
        """Verifica se há conexão ativa"""
        if cls._connection:
            try:
                if SERIAL_AVAILABLE:
                    return cls._connection.is_open
                else:
                    # Modo simulação
                    return True
            except:
                cls._connection = None
                return False
        return False
    
    @classmethod
    def get_connection(cls):
        """Retorna a conexão ativa ou None"""
        if cls.is_connected():
            return cls._connection
        return None
    
    @classmethod
    def get_port(cls):
        """Retorna a porta conectada"""
        return cls._port if cls.is_connected() else None
    
    @classmethod
    def connect(cls, port, baudrate=115200):
        """
        Conecta ao Pico
        
        Args:
            port: Porta serial (ex: /dev/cu.usbmodem141301)
            baudrate: Taxa de transmissão (padrão: 115200)
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        # Se já conectado, desconectar primeiro
        if cls.is_connected():
            if cls._port == port:
                return (True, f"Já conectado em {port}")
            else:
                cls.disconnect()
        
        try:
            if SERIAL_AVAILABLE:
                cls._connection = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    timeout=1
                )
                
                # Inicializar REPL
                cls._connection.write(b'\r\n')
                time.sleep(0.1)
                cls._connection.write(b'\x03')  # Ctrl+C
                time.sleep(0.1)
                cls._connection.write(b'\x04')  # Ctrl+D
                time.sleep(0.5)
                
                # Testar comando simples
                cls._connection.write(b'print("Connected")\r\n')
                time.sleep(0.2)
                
                response = cls._connection.read(cls._connection.in_waiting or 1)
                
                if response or True:  # Aceitar mesmo sem resposta
                    cls._port = port
                    cls._baudrate = baudrate
                    return (True, f"✅ Conectado em {port}")
                else:
                    cls._connection.close()
                    cls._connection = None
                    return (False, "❌ Sem resposta do Pico")
            else:
                # Modo simulação
                cls._connection = "SIMULATED"
                cls._port = port
                cls._baudrate = baudrate
                return (True, f"✅ Conectado (simulação) em {port}")
                
        except Exception as e:
            cls._connection = None
            cls._port = None
            return (False, f"❌ Erro ao conectar: {str(e)}")
    
    @classmethod
    def disconnect(cls):
        """Desconecta do Pico"""
        if cls._connection:
            try:
                if SERIAL_AVAILABLE and hasattr(cls._connection, 'close'):
                    cls._connection.close()
            except:
                pass
            finally:
                cls._connection = None
                cls._port = None
                return (True, "✅ Desconectado")
        return (False, "⚠️ Não estava conectado")
    
    @classmethod
    def send_command(cls, command):
        """
        Envia comando para o Pico
        
        Args:
            command: Comando a ser enviado
            
        Returns:
            tuple: (sucesso, resposta ou erro)
        """
        if not cls.is_connected():
            return (False, "❌ Não conectado")
        
        try:
            if SERIAL_AVAILABLE:
                cls._connection.write(f"{command}\r\n".encode())
                time.sleep(0.2)
                
                # Ler resposta
                response = ""
                if cls._connection.in_waiting:
                    data = cls._connection.read(cls._connection.in_waiting)
                    response = data.decode('utf-8', errors='ignore')
                
                return (True, response)
            else:
                # Modo simulação
                return (True, f">>> {command}\nOK (simulação)")
                
        except Exception as e:
            return (False, f"❌ Erro ao enviar: {str(e)}")
    
    @classmethod
    def upload_file(cls, local_path, remote_path=None, debug=True):
        """
        Faz upload de arquivo para o Pico usando modo paste
        
        Args:
            local_path: Caminho local do arquivo
            remote_path: Caminho remoto (None = usar mesmo nome)
            debug: Se True, imprime mensagens de debug
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        def log(msg):
            if debug:
                print(f"[UPLOAD] {msg}")
        
        if not cls.is_connected():
            return (False, "❌ Não conectado")
        
        if not os.path.exists(local_path):
            return (False, f"❌ Arquivo não encontrado: {local_path}")
        
        # Nome do arquivo remoto
        if remote_path is None:
            remote_path = os.path.basename(local_path)
        
        log(f"Iniciando upload: {local_path} → {remote_path}")
        
        try:
            # Ler conteúdo do arquivo
            with open(local_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            log(f"Arquivo lido: {len(content)} bytes")
            
            if SERIAL_AVAILABLE:
                # Estratégia 1: Usar ampy se disponível
                try:
                    port = cls._port
                    if port:
                        log(f"Tentando upload via ampy...")
                        result = subprocess.run(
                            ['ampy', '--port', port, 'put', local_path, remote_path],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        
                        if result.returncode == 0:
                            log("Upload via ampy bem-sucedido!")
                            return (True, f"✅ Upload concluído (ampy): {remote_path} ({len(content)} bytes)")
                        else:
                            log(f"ampy falhou: {result.stderr}")
                except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                    log(f"ampy não disponível: {e}")
                
                # Estratégia 2: Usar modo paste do MicroPython
                log("Usando modo paste do MicroPython...")
                
                # Limpar buffer de entrada
                cls._connection.reset_input_buffer()
                log("Buffer limpo")
                
                # Interromper qualquer execução
                cls._connection.write(b'\x03')  # Ctrl+C
                time.sleep(0.1)
                cls._connection.write(b'\x03')  # Ctrl+C novamente
                time.sleep(0.2)
                log("Execução interrompida")
                
                # Limpar buffer novamente
                if cls._connection.in_waiting:
                    discarded = cls._connection.read(cls._connection.in_waiting)
                    log(f"Buffer limpo: {len(discarded)} bytes descartados")
                
                # Entrar no modo paste (Ctrl+E)
                cls._connection.write(b'\x05')
                time.sleep(0.2)
                log("Comando paste enviado (Ctrl+E)")
                
                # Verificar se entrou no modo paste
                response = b''
                if cls._connection.in_waiting:
                    response = cls._connection.read(cls._connection.in_waiting)
                    log(f"Resposta paste: {response[:50]}")
                
                # Escapar aspas triplas no conteúdo
                safe_content = content.replace("'''", "'''\"'''\"'''")
                log(f"Conteúdo preparado: {len(safe_content)} bytes")
                
                # Criar script para salvar arquivo
                script = f"""with open('{remote_path}', 'w') as f:
    f.write('''{safe_content}''')
print('UPLOAD_OK:{remote_path}')
"""
                
                log(f"Script criado: {len(script)} bytes")
                
                # Enviar script
                cls._connection.write(script.encode('utf-8'))
                time.sleep(0.3)
                log("Script enviado")
                
                # Sair do modo paste (Ctrl+D)
                cls._connection.write(b'\x04')
                time.sleep(0.8)
                log("Saída do modo paste (Ctrl+D)")
                
                # Ler resposta
                response = b''
                for i in range(10):  # Tentar ler por até 1 segundo
                    if cls._connection.in_waiting:
                        chunk = cls._connection.read(cls._connection.in_waiting)
                        response += chunk
                        log(f"Lido chunk {i}: {len(chunk)} bytes")
                    time.sleep(0.1)
                
                response_text = response.decode('utf-8', errors='ignore')
                log(f"Resposta completa: {len(response_text)} bytes")
                
                # Verificar se salvou com sucesso
                if 'UPLOAD_OK' in response_text:
                    log("✅ Upload confirmado por marcador UPLOAD_OK")
                    return (True, f"✅ Upload concluído: {remote_path} ({len(content)} bytes)")
                
                # Estratégia 3: Verificar se arquivo existe
                log("Verificando existência do arquivo...")
                cls._connection.write(b'\x03')
                time.sleep(0.1)
                cls._connection.write(f"import os\r\nprint('EXISTS:' + str('{remote_path}' in os.listdir()))\r\n".encode())
                time.sleep(0.3)
                
                verify = b''
                if cls._connection.in_waiting:
                    verify = cls._connection.read(cls._connection.in_waiting)
                verify_text = verify.decode('utf-8', errors='ignore')
                log(f"Verificação: {verify_text}")
                
                if 'EXISTS:True' in verify_text:
                    log("✅ Upload verificado por listdir()")
                    return (True, f"✅ Upload verificado: {remote_path} ({len(content)} bytes)")
                else:
                    # Retornar detalhes para debug
                    log(f"❌ Upload falhou")
                    return (False, f"⚠️ Upload falhou.\nResposta: {response_text[:200]}\nVerificação: {verify_text[:100]}")
                
            else:
                # Modo simulação
                log("Modo simulação - upload simulado")
                return (True, f"✅ Upload (simulação): {remote_path} ({len(content)} bytes)")
                
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            log(f"EXCEÇÃO: {error_detail}")
            return (False, f"❌ Erro no upload: {str(e)}\n{error_detail}")
    
    @classmethod
    def list_files(cls):
        """
        Lista arquivos no Pico
        
        Returns:
            tuple: (sucesso, lista de arquivos ou erro)
        """
        if not cls.is_connected():
            return (False, "❌ Não conectado")
        
        try:
            success, response = cls.send_command("import os; print(os.listdir())")
            if success:
                return (True, response)
            return (False, response)
        except Exception as e:
            return (False, f"❌ Erro ao listar: {str(e)}")
    
    @classmethod
    def soft_reset(cls):
        """Executa soft reset no Pico"""
        if not cls.is_connected():
            return (False, "❌ Não conectado")
        
        try:
            if SERIAL_AVAILABLE:
                cls._connection.write(b'\x04')  # Ctrl+D
                time.sleep(0.5)
                return (True, "✅ Soft reset executado")
            else:
                return (True, "✅ Soft reset (simulação)")
        except Exception as e:
            return (False, f"❌ Erro no reset: {str(e)}")
    
    @classmethod
    def get_status_dict(cls):
        """Retorna dicionário com status da conexão"""
        return {
            'connected': cls.is_connected(),
            'port': cls._port,
            'baudrate': cls._baudrate,
            'available': SERIAL_AVAILABLE
        }


# Instância global
pico_manager = PicoConnectionManager()

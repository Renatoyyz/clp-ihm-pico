#!/usr/bin/env python3
"""
Gerador de Código para Raspberry Pi Pico
Gera código MicroPython a partir da configuração LADDER
"""

import json
import os
from datetime import datetime

class PicoCodeGenerator:
    """Gerador de código MicroPython para Raspberry Pi Pico"""
    
    def __init__(self):
        self.config_file = "ladder_config.json"
        self.output_dir = "../generated_code"
        
    def generate_all(self, ladder_components, connections, rs485_config, ihm_config):
        """
        Gera todos os arquivos necessários para o Pico
        
        Args:
            ladder_components: Lista de componentes do LADDER
            connections: Lista de conexões entre componentes
            rs485_config: Configurações RS485
            ihm_config: Configurações do IHM
        """
        # Criar diretório de saída
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Gerar arquivo principal (main_.py para desenvolvimento)
        main_code = self.generate_main_code(ladder_components, connections)
        self.save_file("main_.py", main_code)
        
        # Gerar biblioteca RS485
        rs485_code = self.generate_rs485_lib(rs485_config)
        self.save_file("lib_rs485.py", rs485_code)
        
        # Gerar biblioteca IHM
        ihm_code = self.generate_ihm_lib(ihm_config)
        self.save_file("lib_ihm.py", ihm_code)
        
        # Gerar arquivo de configuração
        config_data = self.generate_config_file(rs485_config, ihm_config)
        self.save_file("config.json", json.dumps(config_data, indent=2))
        
        print(f"✅ Código gerado com sucesso em: {self.output_dir}")
        return True
        
    def generate_rs485_lib(self, rs485_config):
        """Gera biblioteca RS485 para o Pico"""
        if not rs485_config:
            rs485_config = self._get_default_rs485_config()
            
        serial_cfg = rs485_config.get('serial_config', {})
        rs485_cfg = rs485_config.get('rs485_config', {})
        network_cfg = rs485_config.get('network_config', {})
        
        code = f'''"""
Biblioteca RS485 para Raspberry Pi Pico
Gerado automaticamente pelo Editor LADDER
Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from machine import UART, Pin
import time
import struct

class RS485Communication:
    """Classe para comunicação RS485 via Modbus RTU"""
    
    def __init__(self):
        # Configurações Serial/RS232
        self.uart_port = {serial_cfg.get('port', 'UART0').replace('UART', '')}
        self.baudrate = {serial_cfg.get('baudrate', 9600)}
        self.data_bits = {serial_cfg.get('data_bits', 8)}
        self.stop_bits = {serial_cfg.get('stop_bits', 1)}
        self.parity = {self._get_parity_value(serial_cfg.get('parity', 'None'))}
        
        # Configurações RS485
        self.enable_pin = {rs485_cfg.get('enable_pin', 2)}
        self.mode = "{rs485_cfg.get('mode', 'Master')}"
        self.device_address = {rs485_cfg.get('device_address', 1)}
        self.timeout = {rs485_cfg.get('timeout', 1000)}
        self.max_retries = {rs485_cfg.get('max_retries', 3)}
        
        # Protocolo
        self.protocol = "{network_cfg.get('protocol', 'Modbus RTU')}"
        
        # Inicializar hardware
        self._init_hardware()
        
    def _init_hardware(self):
        """Inicializa hardware UART e pino DE/RE"""
        # Configurar UART
        self.uart = UART(
            self.uart_port,
            baudrate=self.baudrate,
            bits=self.data_bits,
            stop=self.stop_bits,
            parity=self.parity
        )
        
        # Configurar pino DE/RE (Direction Enable)
        self.de_pin = Pin(self.enable_pin, Pin.OUT)
        self.de_pin.value(0)  # Modo recepção por padrão
        
        print(f"✅ RS485 inicializado: UART{{self.uart_port}}, {{self.baudrate}} baud")
        
    def set_transmit_mode(self):
        """Configura para modo transmissão"""
        self.de_pin.value(1)
        time.sleep_us(10)  # Pequeno delay para estabilização
        
    def set_receive_mode(self):
        """Configura para modo recepção"""
        time.sleep_us(10)  # Pequeno delay antes de mudar
        self.de_pin.value(0)
        
    def calculate_crc16(self, data):
        """Calcula CRC16 para Modbus RTU"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc
        
    def send_request(self, slave_id, function_code, data):
        """
        Envia requisição Modbus RTU
        
        Args:
            slave_id: Endereço do dispositivo slave (1-247)
            function_code: Código da função Modbus
            data: Dados da requisição
            
        Returns:
            bytes: Resposta do slave ou None se falhar
        """
        # Montar frame Modbus
        frame = bytes([slave_id, function_code]) + data
        crc = self.calculate_crc16(frame)
        frame += struct.pack('<H', crc)  # CRC em little-endian
        
        # Enviar
        self.set_transmit_mode()
        self.uart.write(frame)
        self.uart.flush()
        self.set_receive_mode()
        
        # Aguardar resposta
        start_time = time.ticks_ms()
        response = b''
        
        while time.ticks_diff(time.ticks_ms(), start_time) < self.timeout:
            if self.uart.any():
                response += self.uart.read()
                # Verificar se recebeu resposta completa (mínimo 5 bytes)
                if len(response) >= 5:
                    # Verificar CRC
                    if self._verify_crc(response):
                        return response
            time.sleep_ms(10)
            
        return None
        
    def _verify_crc(self, data):
        """Verifica CRC da resposta"""
        if len(data) < 3:
            return False
        received_crc = struct.unpack('<H', data[-2:])[0]
        calculated_crc = self.calculate_crc16(data[:-2])
        return received_crc == calculated_crc
        
    # Funções Modbus RTU
    
    def read_coils(self, slave_id, start_address, quantity):
        """
        Função 0x01: Ler bobinas (coils)
        
        Args:
            slave_id: Endereço do dispositivo
            start_address: Endereço inicial
            quantity: Quantidade de bobinas (1-2000)
            
        Returns:
            list: Lista de valores booleanos ou None
        """
        data = struct.pack('>HH', start_address, quantity)
        response = self.send_request(slave_id, 0x01, data)
        
        if response and len(response) > 3:
            byte_count = response[2]
            coil_bytes = response[3:3+byte_count]
            
            # Converter bytes para lista de booleanos
            coils = []
            for byte in coil_bytes:
                for bit in range(8):
                    if len(coils) < quantity:
                        coils.append(bool(byte & (1 << bit)))
            return coils[:quantity]
        return None
        
    def read_discrete_inputs(self, slave_id, start_address, quantity):
        """
        Função 0x02: Ler entradas discretas
        
        Args:
            slave_id: Endereço do dispositivo
            start_address: Endereço inicial
            quantity: Quantidade de entradas (1-2000)
            
        Returns:
            list: Lista de valores booleanos ou None
        """
        data = struct.pack('>HH', start_address, quantity)
        response = self.send_request(slave_id, 0x02, data)
        
        if response and len(response) > 3:
            byte_count = response[2]
            input_bytes = response[3:3+byte_count]
            
            # Converter bytes para lista de booleanos
            inputs = []
            for byte in input_bytes:
                for bit in range(8):
                    if len(inputs) < quantity:
                        inputs.append(bool(byte & (1 << bit)))
            return inputs[:quantity]
        return None
        
    def read_holding_registers(self, slave_id, start_address, quantity):
        """
        Função 0x03: Ler registradores holding
        
        Args:
            slave_id: Endereço do dispositivo
            start_address: Endereço inicial
            quantity: Quantidade de registradores (1-125)
            
        Returns:
            list: Lista de valores inteiros (16-bit) ou None
        """
        data = struct.pack('>HH', start_address, quantity)
        response = self.send_request(slave_id, 0x03, data)
        
        if response and len(response) > 3:
            byte_count = response[2]
            registers = []
            for i in range(0, byte_count, 2):
                reg_value = struct.unpack('>H', response[3+i:5+i])[0]
                registers.append(reg_value)
            return registers
        return None
        
    def write_single_coil(self, slave_id, address, value):
        """
        Função 0x05: Escrever bobina única
        
        Args:
            slave_id: Endereço do dispositivo
            address: Endereço da bobina
            value: True (ON) ou False (OFF)
            
        Returns:
            bool: True se sucesso, False se falha
        """
        coil_value = 0xFF00 if value else 0x0000
        data = struct.pack('>HH', address, coil_value)
        response = self.send_request(slave_id, 0x05, data)
        return response is not None
        
    def write_single_register(self, slave_id, address, value):
        """
        Função 0x06: Escrever registrador único
        
        Args:
            slave_id: Endereço do dispositivo
            address: Endereço do registrador
            value: Valor inteiro (0-65535)
            
        Returns:
            bool: True se sucesso, False se falha
        """
        data = struct.pack('>HH', address, value)
        response = self.send_request(slave_id, 0x06, data)
        return response is not None
        
    def write_multiple_registers(self, slave_id, start_address, values):
        """
        Função 0x10: Escrever múltiplos registradores
        
        Args:
            slave_id: Endereço do dispositivo
            start_address: Endereço inicial
            values: Lista de valores inteiros
            
        Returns:
            bool: True se sucesso, False se falha
        """
        quantity = len(values)
        byte_count = quantity * 2
        data = struct.pack('>HHB', start_address, quantity, byte_count)
        for value in values:
            data += struct.pack('>H', value)
        response = self.send_request(slave_id, 0x10, data)
        return response is not None

# Instância global
rs485 = None

def init_rs485():
    """Inicializa comunicação RS485"""
    global rs485
    rs485 = RS485Communication()
    return rs485
'''
        
        return code
        
    def _get_parity_value(self, parity_str):
        """Converte string de paridade para valor do MicroPython"""
        parity_map = {
            'None': 'None',
            'Even': '0',
            'Odd': '1'
        }
        return parity_map.get(parity_str, 'None')
        
    def _get_default_rs485_config(self):
        """Retorna configuração padrão RS485"""
        return {
            'serial_config': {
                'port': 'UART0',
                'baudrate': 9600,
                'data_bits': 8,
                'stop_bits': 1,
                'parity': 'None'
            },
            'rs485_config': {
                'enable_pin': 2,
                'mode': 'Master',
                'device_address': 1,
                'timeout': 1000,
                'max_retries': 3
            },
            'network_config': {
                'protocol': 'Modbus RTU'
            }
        }
        
    def generate_main_code(self, ladder_components, connections):
        """Gera código principal (main_.py)"""
        code = f'''"""
Código LADDER para Raspberry Pi Pico
Gerado automaticamente pelo Editor LADDER
Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

ATENÇÃO: Este arquivo é main_.py durante desenvolvimento.
Para produção, renomear para main.py
"""

import time
from machine import Pin
from lib_rs485 import init_rs485
from lib_ihm import init_ihm

# Inicialização
print("="*50)
print("🚀 Iniciando Sistema LADDER")
print("="*50)

# Inicializar RS485
print("📡 Inicializando RS485...")
rs485 = init_rs485()

# Inicializar IHM
print("🖥️ Inicializando IHM...")
ihm = init_ihm()

# Variáveis do sistema
print("💾 Inicializando variáveis...")

# TODO: Inicializar variáveis baseadas nos componentes LADDER

print("✅ Sistema inicializado com sucesso!")
print("="*50)

# Loop principal
print("🔄 Entrando no loop principal...")
while True:
    try:
        # TODO: Lógica LADDER será gerada aqui
        
        # Delay pequeno para não sobrecarregar CPU
        time.sleep_ms(10)
        
    except KeyboardInterrupt:
        print("\\n⚠️ Sistema interrompido pelo usuário")
        break
    except Exception as e:
        print(f"❌ Erro no loop principal: {{e}}")
        time.sleep(1)

print("👋 Sistema encerrado")
'''
        return code
        
    def generate_ihm_lib(self, ihm_config):
        """Gera biblioteca IHM para o Pico"""
        code = f'''"""
Biblioteca IHM para Raspberry Pi Pico
Display ST7920 128x64
Gerado automaticamente pelo Editor LADDER
Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from machine import Pin, SPI
import time

class ST7920Display:
    """Driver para display ST7920 128x64"""
    
    def __init__(self, spi_id=0, cs_pin=17, rst_pin=None):
        self.width = 128
        self.height = 64
        
        # Configurar SPI
        self.spi = SPI(spi_id, baudrate=1000000, polarity=0, phase=0)
        self.cs = Pin(cs_pin, Pin.OUT)
        self.cs.value(1)
        
        # Reset (opcional)
        if rst_pin:
            self.rst = Pin(rst_pin, Pin.OUT)
            self.reset()
            
        self.init_display()
        
    def reset(self):
        """Reset do display"""
        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        time.sleep_ms(50)
        
    def init_display(self):
        """Inicializa display ST7920"""
        # TODO: Comandos de inicialização do ST7920
        print("🖥️ Display ST7920 inicializado")
        
    def clear(self):
        """Limpa display"""
        # TODO: Implementar limpeza
        pass
        
    def write_text(self, x, y, text):
        """Escreve texto no display"""
        # TODO: Implementar escrita de texto
        pass

# Instância global
ihm = None

def init_ihm():
    """Inicializa display IHM"""
    global ihm
    ihm = ST7920Display()
    return ihm
'''
        return code
        
    def generate_config_file(self, rs485_config, ihm_config):
        """Gera arquivo de configuração JSON"""
        config = {
            'version': '1.0',
            'generated_at': datetime.now().isoformat(),
            'rs485': rs485_config if rs485_config else {},
            'ihm': ihm_config if ihm_config else {},
            'ladder': {
                'scan_time_ms': 10,
                'components': [],
                'connections': []
            }
        }
        return config
        
    def save_file(self, filename, content):
        """Salva arquivo no diretório de saída"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Arquivo gerado: {filepath}")

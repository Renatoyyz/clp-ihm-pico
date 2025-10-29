"""
Biblioteca RS485 para Raspberry Pi Pico
Gerado automaticamente pelo Editor LADDER
Data: 2025-10-29 11:07:26
"""

from machine import UART, Pin
import time
import struct

class RS485Communication:
    """Classe para comunicação RS485 via Modbus RTU"""
    
    def __init__(self):
        # Configurações Serial/RS232
        self.uart_port = 0
        self.baudrate = 9600
        self.data_bits = 8
        self.stop_bits = 1
        self.parity = None
        
        # Configurações RS485
        self.enable_pin = 0
        self.mode = "Master"
        self.device_address = 1
        self.timeout = 1000
        self.max_retries = 3
        
        # Protocolo
        self.protocol = "Modbus RTU"
        
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
        
        print(f"✅ RS485 inicializado: UART{self.uart_port}, {self.baudrate} baud")
        
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

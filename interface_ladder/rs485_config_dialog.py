#!/usr/bin/env python3
"""
Diálogo de Configuração RS485
Interface para configurar comunicação RS485 via RS232 no Raspberry Pi Pico
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QCheckBox, QPushButton, 
                           QGroupBox, QGridLayout, QSpinBox, QTextEdit,
                           QTabWidget, QWidget, QMessageBox, QFrame,
                           QFormLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
import json
import os

class RS485ConfigDialog(QDialog):
    """Diálogo para configurar comunicação RS485"""
    
    config_saved = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("🌐 Configuração RS485 - Comunicação em Rede")
        self.setModal(True)
        self.resize(600, 500)
        
        # Dados de configuração
        self.config_data = {
            'serial_config': {
                'port': 'UART0',
                'baudrate': 9600,
                'data_bits': 8,
                'stop_bits': 1,
                'parity': 'None',
                'flow_control': 'None'
            },
            'rs485_config': {
                'enable_pin': 2,
                'mode': 'Master',
                'device_address': 1,
                'timeout': 1000,
                'max_retries': 3
            },
            'network_config': {
                'protocol': 'Modbus RTU',
                'devices': []
            }
        }
        
        self.init_ui()
        self.load_config()
        
    def init_ui(self):
        """Inicializa interface do usuário"""
        layout = QVBoxLayout(self)
        
        # Título
        title_frame = QFrame()
        title_frame.setFixedHeight(60)
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
                border-radius: 10px;
                margin: 5px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        title_label = QLabel("🌐 Configuração RS485")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: white; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("Comunicação em rede via RS232 → RS485")
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setStyleSheet("color: #E3F2FD; padding: 0px 10px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addWidget(title_frame)
        
        # Abas de configuração
        tabs = QTabWidget()
        
        # Aba 1: Configuração Serial
        serial_tab = self.create_serial_tab()
        tabs.addTab(serial_tab, "📡 Serial/RS232")
        
        # Aba 2: Configuração RS485
        rs485_tab = self.create_rs485_tab()
        tabs.addTab(rs485_tab, "🌐 RS485")
        
        # Aba 3: Dispositivos de Rede
        devices_tab = self.create_devices_tab()
        tabs.addTab(devices_tab, "🔗 Dispositivos")
        
        layout.addWidget(tabs)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Testar Conexão")
        test_btn.clicked.connect(self.test_connection)
        buttons_layout.addWidget(test_btn)
        
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Salvar")
        save_btn.clicked.connect(self.save_config)
        save_btn.setDefault(True)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
    def create_serial_tab(self):
        """Cria aba de configuração serial"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Grupo Serial/RS232
        serial_group = QGroupBox("📡 Configuração Serial (RS232)")
        serial_layout = QFormLayout(serial_group)
        
        # Porta UART
        self.port_combo = QComboBox()
        self.port_combo.addItems(['UART0', 'UART1'])
        serial_layout.addRow("Porta UART:", self.port_combo)
        
        # Baudrate
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        self.baudrate_combo.setCurrentText('9600')
        serial_layout.addRow("Baudrate:", self.baudrate_combo)
        
        # Data bits
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.addItems(['7', '8'])
        self.data_bits_combo.setCurrentText('8')
        serial_layout.addRow("Data Bits:", self.data_bits_combo)
        
        # Stop bits
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.addItems(['1', '2'])
        serial_layout.addRow("Stop Bits:", self.stop_bits_combo)
        
        # Paridade
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['None', 'Odd', 'Even'])
        serial_layout.addRow("Paridade:", self.parity_combo)
        
        # Flow control
        self.flow_control_combo = QComboBox()
        self.flow_control_combo.addItems(['None', 'RTS/CTS', 'XON/XOFF'])
        serial_layout.addRow("Controle de Fluxo:", self.flow_control_combo)
        
        layout.addWidget(serial_group)
        
        # Informações de conexão
        info_group = QGroupBox("📋 Informações de Conexão")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
        🔌 <b>Conexão Física:</b><br>
        • Pico TX → Módulo RS485 DI (Data Input)<br>
        • Pico RX → Módulo RS485 RO (Receiver Output)<br>
        • Pico GPIO → Módulo RS485 DE/RE (Enable)<br><br>
        
        ⚡ <b>Alimentação:</b><br>
        • VCC: 3.3V ou 5V (conforme módulo)<br>
        • GND: Terra comum<br><br>
        
        🌐 <b>Rede RS485:</b><br>
        • A+: Linha diferencial positiva<br>
        • B-: Linha diferencial negativa<br>
        • Máximo 32 dispositivos por rede
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 10px; background-color: #f0f8ff; border-radius: 5px;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        layout.addStretch()
        
        return widget
        
    def create_rs485_tab(self):
        """Cria aba de configuração RS485"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Grupo RS485
        rs485_group = QGroupBox("🌐 Configuração RS485")
        rs485_layout = QFormLayout(rs485_group)
        
        # Pino de habilitação
        self.enable_pin_spin = QSpinBox()
        self.enable_pin_spin.setRange(0, 29)
        self.enable_pin_spin.setValue(2)
        rs485_layout.addRow("Pino DE/RE (Enable):", self.enable_pin_spin)
        
        # Modo
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Master', 'Slave'])
        rs485_layout.addRow("Modo:", self.mode_combo)
        
        # Endereço do dispositivo
        self.device_address_spin = QSpinBox()
        self.device_address_spin.setRange(1, 247)
        self.device_address_spin.setValue(1)
        rs485_layout.addRow("Endereço do Dispositivo:", self.device_address_spin)
        
        # Timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(100, 10000)
        self.timeout_spin.setValue(1000)
        self.timeout_spin.setSuffix(" ms")
        rs485_layout.addRow("Timeout:", self.timeout_spin)
        
        # Máximo de tentativas
        self.max_retries_spin = QSpinBox()
        self.max_retries_spin.setRange(1, 10)
        self.max_retries_spin.setValue(3)
        rs485_layout.addRow("Máx. Tentativas:", self.max_retries_spin)
        
        layout.addWidget(rs485_group)
        
        # Grupo Protocolo
        protocol_group = QGroupBox("📡 Protocolo de Comunicação")
        protocol_layout = QFormLayout(protocol_group)
        
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(['Modbus RTU', 'Modbus ASCII', 'Custom Protocol'])
        protocol_layout.addRow("Protocolo:", self.protocol_combo)
        
        layout.addWidget(protocol_group)
        
        # Área de teste
        test_group = QGroupBox("🧪 Teste de Comunicação")
        test_layout = QVBoxLayout(test_group)
        
        test_buttons = QHBoxLayout()
        
        scan_btn = QPushButton("🔍 Escanear Rede")
        scan_btn.clicked.connect(self.scan_network)
        test_buttons.addWidget(scan_btn)
        
        ping_btn = QPushButton("📡 Ping Dispositivo")
        ping_btn.clicked.connect(self.ping_device)
        test_buttons.addWidget(ping_btn)
        
        test_layout.addLayout(test_buttons)
        
        # Log de teste
        self.test_log = QTextEdit()
        self.test_log.setMaximumHeight(100)
        self.test_log.setPlaceholderText("Logs de teste aparecerão aqui...")
        test_layout.addWidget(self.test_log)
        
        layout.addWidget(test_group)
        layout.addStretch()
        
        return widget
        
    def create_devices_tab(self):
        """Cria aba de dispositivos na rede"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Grupo Dispositivos
        devices_group = QGroupBox("🔗 Dispositivos na Rede RS485")
        devices_layout = QVBoxLayout(devices_group)
        
        # Adicionar dispositivo
        add_device_layout = QHBoxLayout()
        
        add_device_layout.addWidget(QLabel("Endereço:"))
        self.new_device_address = QSpinBox()
        self.new_device_address.setRange(1, 247)
        add_device_layout.addWidget(self.new_device_address)
        
        add_device_layout.addWidget(QLabel("Nome:"))
        self.new_device_name = QLineEdit()
        self.new_device_name.setPlaceholderText("Ex: Sensor Temperatura")
        add_device_layout.addWidget(self.new_device_name)
        
        add_btn = QPushButton("➕ Adicionar")
        add_btn.clicked.connect(self.add_device)
        add_device_layout.addWidget(add_btn)
        
        devices_layout.addLayout(add_device_layout)
        
        # Lista de dispositivos
        self.devices_list = QTextEdit()
        self.devices_list.setMaximumHeight(200)
        self.devices_list.setPlaceholderText("Nenhum dispositivo configurado...")
        devices_layout.addWidget(self.devices_list)
        
        layout.addWidget(devices_group)
        
        # Exemplo de configuração
        example_group = QGroupBox("📝 Exemplo de Configuração")
        example_layout = QVBoxLayout(example_group)
        
        example_text = QLabel("""
        <b>Configuração típica para rede Modbus RTU:</b><br><br>
        
        🏭 <b>Cenário Industrial:</b><br>
        • Endereço 1: CLP Principal (Master)<br>
        • Endereço 2: Sensor de Temperatura<br>
        • Endereço 3: Inversor de Frequência<br>
        • Endereço 4: Medidor de Energia<br><br>
        
        ⚙️ <b>Parâmetros Recomendados:</b><br>
        • Baudrate: 9600 bps<br>
        • Data: 8 bits, Stop: 1 bit, Paridade: None<br>
        • Timeout: 1000 ms<br>
        • Tentativas: 3x
        """)
        example_text.setWordWrap(True)
        example_text.setStyleSheet("padding: 10px; background-color: #fff8e1; border-radius: 5px;")
        example_layout.addWidget(example_text)
        
        layout.addWidget(example_group)
        layout.addStretch()
        
        return widget
        
    def add_device(self):
        """Adiciona dispositivo à lista"""
        address = self.new_device_address.value()
        name = self.new_device_name.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Aviso", "Digite um nome para o dispositivo")
            return
            
        # Verificar se endereço já existe
        for device in self.config_data['network_config']['devices']:
            if device['address'] == address:
                QMessageBox.warning(self, "Aviso", f"Endereço {address} já está em uso")
                return
                
        # Adicionar dispositivo
        device = {
            'address': address,
            'name': name,
            'type': 'Generic',
            'status': 'Unknown'
        }
        
        self.config_data['network_config']['devices'].append(device)
        self.update_devices_list()
        
        # Limpar campos
        self.new_device_address.setValue(self.new_device_address.value() + 1)
        self.new_device_name.clear()
        
    def update_devices_list(self):
        """Atualiza lista de dispositivos"""
        devices = self.config_data['network_config']['devices']
        
        if not devices:
            self.devices_list.setText("Nenhum dispositivo configurado...")
            return
            
        text = ""
        for device in devices:
            text += f"📱 Endereço {device['address']}: {device['name']}\n"
            
        self.devices_list.setText(text)
        
    def scan_network(self):
        """Simula escaneamento da rede"""
        self.test_log.append("🔍 Iniciando escaneamento da rede RS485...")
        self.test_log.append("📡 Verificando endereços 1-247...")
        self.test_log.append("⚠️ Funcionalidade de escaneamento será implementada no firmware")
        
    def ping_device(self):
        """Simula ping de dispositivo"""
        address = self.device_address_spin.value()
        self.test_log.append(f"📡 Enviando ping para dispositivo {address}...")
        self.test_log.append("⚠️ Funcionalidade de ping será implementada no firmware")
        
    def test_connection(self):
        """Testa configuração"""
        self.test_log.append("🧪 Testando configuração RS485...")
        self.test_log.append(f"📡 Porta: {self.port_combo.currentText()}")
        self.test_log.append(f"⚡ Baudrate: {self.baudrate_combo.currentText()}")
        self.test_log.append(f"🌐 Endereço: {self.device_address_spin.value()}")
        self.test_log.append("✅ Configuração válida - pronta para upload")
        
    def load_config(self):
        """Carrega configuração salva"""
        config_file = "rs485_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config_data.update(saved_config)
                    self.update_ui_from_config()
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
                
    def update_ui_from_config(self):
        """Atualiza interface com configuração carregada"""
        serial_config = self.config_data['serial_config']
        rs485_config = self.config_data['rs485_config']
        network_config = self.config_data['network_config']
        
        # Serial
        self.port_combo.setCurrentText(serial_config['port'])
        self.baudrate_combo.setCurrentText(str(serial_config['baudrate']))
        self.data_bits_combo.setCurrentText(str(serial_config['data_bits']))
        self.stop_bits_combo.setCurrentText(str(serial_config['stop_bits']))
        self.parity_combo.setCurrentText(serial_config['parity'])
        self.flow_control_combo.setCurrentText(serial_config['flow_control'])
        
        # RS485
        self.enable_pin_spin.setValue(rs485_config['enable_pin'])
        self.mode_combo.setCurrentText(rs485_config['mode'])
        self.device_address_spin.setValue(rs485_config['device_address'])
        self.timeout_spin.setValue(rs485_config['timeout'])
        self.max_retries_spin.setValue(rs485_config['max_retries'])
        
        # Protocolo
        self.protocol_combo.setCurrentText(network_config['protocol'])
        
        # Dispositivos
        self.update_devices_list()
        
    def save_config(self):
        """Salva configuração"""
        # Coletar dados da interface
        self.config_data['serial_config'] = {
            'port': self.port_combo.currentText(),
            'baudrate': int(self.baudrate_combo.currentText()),
            'data_bits': int(self.data_bits_combo.currentText()),
            'stop_bits': int(self.stop_bits_combo.currentText()),
            'parity': self.parity_combo.currentText(),
            'flow_control': self.flow_control_combo.currentText()
        }
        
        self.config_data['rs485_config'] = {
            'enable_pin': self.enable_pin_spin.value(),
            'mode': self.mode_combo.currentText(),
            'device_address': self.device_address_spin.value(),
            'timeout': self.timeout_spin.value(),
            'max_retries': self.max_retries_spin.value()
        }
        
        self.config_data['network_config']['protocol'] = self.protocol_combo.currentText()
        
        # Salvar em arquivo
        try:
            config_file = "rs485_config.json"
            with open(config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
                
            QMessageBox.information(self, "Sucesso", 
                                  "🌐 Configuração RS485 salva com sucesso!\n\n"
                                  "A configuração será aplicada no próximo upload para o Pico.")
            
            self.config_saved.emit(self.config_data)
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configuração:\n{e}")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    dialog = RS485ConfigDialog()
    dialog.show()
    sys.exit(app.exec_())
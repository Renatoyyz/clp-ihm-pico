#!/usr/bin/env python3
"""
Diálogo de Configuração e Conexão com Raspberry Pi Pico
Sistema completo de detecção, conexão e monitoramento
"""

import sys
import os
import time
import threading
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QPushButton, QComboBox, QTextEdit, QProgressBar,
    QCheckBox, QSpinBox, QTabWidget, QWidget, QSplitter,
    QListWidget, QListWidgetItem, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QColor, QPalette

# Importar gerenciador de conexão
from pico_connection_manager import pico_manager, SERIAL_AVAILABLE

# Importar suporte para comunicação serial (para detecção de portas)
try:
    import serial
    import serial.tools.list_ports
except ImportError:
    pass


class PortScannerThread(QThread):
    """Thread para escaneamento contínuo de portas"""
    ports_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        """Executa escaneamento de portas"""
        while self.running:
            if SERIAL_AVAILABLE:
                ports = list(serial.tools.list_ports.comports())
                port_info = []
                for port in ports:
                    # Detectar se é um Raspberry Pi Pico
                    is_pico = self.detect_pico(port)
                    port_info.append({
                        'device': port.device,
                        'description': port.description,
                        'hwid': port.hwid,
                        'is_pico': is_pico
                    })
                self.ports_updated.emit(port_info)
            else:
                # Modo simulação
                fake_ports = [
                    {'device': '/dev/cu.usbmodem101', 'description': 'USB Serial Device', 'hwid': 'USB VID:PID=1234:5678', 'is_pico': False},
                    {'device': '/dev/cu.usbmodem141301', 'description': 'Board in FS mode', 'hwid': 'USB VID:PID=2E8A:0005', 'is_pico': True},
                    {'device': '/dev/cu.Bluetooth-Incoming-Port', 'description': 'Bluetooth Device', 'hwid': 'BLUETOOTH', 'is_pico': False}
                ]
                self.ports_updated.emit(fake_ports)
            
            self.msleep(2000)  # Escanear a cada 2 segundos
            
    def detect_pico(self, port):
        """Detecta se a porta é um Raspberry Pi Pico"""
        pico_indicators = [
            'Board in FS mode',
            'Pico',
            'MicroPython',
            '2E8A:0005',  # VID:PID do Pico em modo CircuitPython/MicroPython
            '2E8A:000A',  # VID:PID do Pico em modo FS
        ]
        
        port_text = f"{port.description} {port.hwid}".lower()
        return any(indicator.lower() in port_text for indicator in pico_indicators)
        
    def stop(self):
        """Para o escaneamento"""
        self.running = False


class PicoConnectionThread(QThread):
    """Thread para conexão com o Pico"""
    connection_result = pyqtSignal(bool, str, str)
    output_received = pyqtSignal(str)
    
    def __init__(self, port, baudrate=115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        
    def run(self):
        """Tenta conectar com o Pico"""
        try:
            if SERIAL_AVAILABLE:
                self.connection = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=1
                )
                
                # Tentar inicializar REPL
                self.connection.write(b'\r\n')
                time.sleep(0.1)
                self.connection.write(b'\x03')  # Ctrl+C
                time.sleep(0.1)
                self.connection.write(b'\x04')  # Ctrl+D
                time.sleep(0.5)
                
                # Testar comando simples
                self.connection.write(b'print("Pico conectado!")\r\n')
                time.sleep(0.2)
                
                response = self.connection.read(self.connection.in_waiting or 1)
                
                if response:
                    self.connection_result.emit(True, self.port, "Conexão estabelecida com sucesso")
                    
                    # Continuar lendo saídas
                    self.monitor_output()
                else:
                    self.connection_result.emit(False, self.port, "Sem resposta do Pico")
            else:
                # Modo simulação
                time.sleep(1)
                self.connection_result.emit(True, self.port, "Conexão simulada estabelecida")
                
        except Exception as e:
            self.connection_result.emit(False, self.port, f"Erro: {str(e)}")
            
    def monitor_output(self):
        """Monitora saída do Pico"""
        while self.connection and self.connection.is_open:
            try:
                if self.connection.in_waiting:
                    data = self.connection.read(self.connection.in_waiting)
                    if data:
                        text = data.decode('utf-8', errors='ignore')
                        self.output_received.emit(text)
                self.msleep(100)
            except:
                break
                
    def send_command(self, command):
        """Envia comando para o Pico"""
        if self.connection and self.connection.is_open:
            self.connection.write(f"{command}\r\n".encode())
        
    def disconnect(self):
        """Desconecta do Pico"""
        if self.connection and self.connection.is_open:
            self.connection.close()


class ConfigDialog(QDialog):
    """Diálogo de configuração de conexão com Pico"""
    
    connection_changed = pyqtSignal(bool, str)
    log_message = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.port_scanner = None
        self.connection_thread = None
        self.current_connection = None
        self.init_ui()
        
        # Verificar se já existe conexão ativa
        self.check_existing_connection()
        
        self.start_port_scanner()
        
    def init_ui(self):
        """Inicializa interface do usuário"""
        self.setWindowTitle("🔌 Configuração Conexão Pico")
        self.setGeometry(200, 200, 800, 600)
        self.setModal(False)  # Permitir usar outras janelas
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Criar abas
        tabs = QTabWidget()
        
        # Aba de Conexão
        connection_tab = self.create_connection_tab()
        tabs.addTab(connection_tab, "🔌 Conexão")
        
        # Aba de Monitor
        monitor_tab = self.create_monitor_tab()
        tabs.addTab(monitor_tab, "📺 Monitor")
        
        # Aba de Testes
        test_tab = self.create_test_tab()
        tabs.addTab(test_tab, "🧪 Testes")
        
        layout.addWidget(tabs)
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("🔌 Conectar")
        self.connect_btn.clicked.connect(self.connect_to_pico)
        button_layout.addWidget(self.connect_btn)
        
        self.disconnect_btn = QPushButton("❌ Desconectar")
        self.disconnect_btn.clicked.connect(self.disconnect_from_pico)
        self.disconnect_btn.setEnabled(False)
        button_layout.addWidget(self.disconnect_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("✅ Fechar")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Aplicar estilo
        self.apply_style()
        
    def create_connection_tab(self):
        """Cria aba de conexão"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Grupo de detecção de portas
        ports_group = QGroupBox("📡 Detecção de Portas")
        ports_layout = QVBoxLayout(ports_group)
        
        # Status da detecção
        self.detection_status = QLabel("🔍 Escaneando portas...")
        ports_layout.addWidget(self.detection_status)
        
        # Lista de portas
        self.ports_list = QListWidget()
        self.ports_list.setMaximumHeight(150)
        ports_layout.addWidget(self.ports_list)
        
        # Refresh manual
        refresh_btn = QPushButton("🔄 Atualizar Lista")
        refresh_btn.clicked.connect(self.refresh_ports)
        ports_layout.addWidget(refresh_btn)
        
        layout.addWidget(ports_group)
        
        # Grupo de configuração
        config_group = QGroupBox("⚙️ Configuração da Conexão")
        config_layout = QGridLayout(config_group)
        
        # Porta selecionada
        config_layout.addWidget(QLabel("Porta:"), 0, 0)
        self.port_combo = QComboBox()
        self.port_combo.setEditable(True)
        config_layout.addWidget(self.port_combo, 0, 1)
        
        # Baudrate
        config_layout.addWidget(QLabel("Baudrate:"), 1, 0)
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(['115200', '9600', '19200', '38400', '57600'])
        self.baudrate_combo.setCurrentText('115200')
        config_layout.addWidget(self.baudrate_combo, 1, 1)
        
        # Auto-conectar
        self.auto_connect_cb = QCheckBox("Conectar automaticamente ao detectar Pico")
        config_layout.addWidget(self.auto_connect_cb, 2, 0, 1, 2)
        
        # Timeout
        config_layout.addWidget(QLabel("Timeout (s):"), 3, 0)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(1)
        self.timeout_spin.setMaximum(30)
        self.timeout_spin.setValue(5)
        config_layout.addWidget(self.timeout_spin, 3, 1)
        
        layout.addWidget(config_group)
        
        # Status da conexão
        status_group = QGroupBox("📊 Status da Conexão")
        status_layout = QVBoxLayout(status_group)
        
        self.connection_status = QLabel("🔴 Desconectado")
        self.connection_status.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(self.connection_status)
        
        self.connection_details = QLabel("Aguardando conexão...")
        status_layout.addWidget(self.connection_details)
        
        layout.addWidget(status_group)
        
        layout.addStretch()
        return widget
        
    def create_monitor_tab(self):
        """Cria aba de monitoramento"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Área de saída do Pico
        output_group = QGroupBox("📺 Saída do Raspberry Pi Pico")
        output_layout = QVBoxLayout(output_group)
        
        self.pico_output = QTextEdit()
        self.pico_output.setFont(QFont("Courier New", 10))
        self.pico_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #555;
            }
        """)
        self.pico_output.setPlainText("📡 Aguardando conexão com Pico...\n")
        output_layout.addWidget(self.pico_output)
        
        # Controles do monitor
        control_layout = QHBoxLayout()
        
        clear_btn = QPushButton("🗑️ Limpar")
        clear_btn.clicked.connect(self.clear_output)
        control_layout.addWidget(clear_btn)
        
        save_btn = QPushButton("💾 Salvar Log")
        save_btn.clicked.connect(self.save_log)
        control_layout.addWidget(save_btn)
        
        control_layout.addStretch()
        
        auto_scroll_cb = QCheckBox("Auto-scroll")
        auto_scroll_cb.setChecked(True)
        self.auto_scroll = auto_scroll_cb
        control_layout.addWidget(auto_scroll_cb)
        
        output_layout.addLayout(control_layout)
        layout.addWidget(output_group)
        
        return widget
        
    def create_test_tab(self):
        """Cria aba de testes"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Comandos de teste
        commands_group = QGroupBox("🧪 Comandos de Teste")
        commands_layout = QVBoxLayout(commands_group)
        
        # Botões de teste
        test_layout = QGridLayout()
        
        test_buttons = [
            ("💡 LED Pico", "pin = Pin('LED', Pin.OUT); pin.on()"),
            ("💡 LED OFF", "pin.off()"),
            ("🌡️ Temperatura", "from machine import ADC; sensor = ADC(4); temp = 27 - (sensor.read_u16() * 3.3 / 65536 - 0.706) / 0.001721; print(f'Temp: {temp:.1f}°C')"),
            ("🔢 Versão", "import sys; print(sys.version)"),
            ("💾 Memória", "import gc; gc.collect(); print(f'Mem livre: {gc.mem_free()} bytes')"),
            ("📁 Arquivos", "import os; print(os.listdir())"),
            ("🔄 Reset Soft", "import machine; machine.soft_reset()"),
            ("⚡ Teste GPIO", "from machine import Pin; led = Pin(25, Pin.OUT); [led.toggle() for _ in range(5)]")
        ]
        
        for i, (name, command) in enumerate(test_buttons):
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, cmd=command: self.send_test_command(cmd))
            test_layout.addWidget(btn, i // 2, i % 2)
            
        commands_layout.addLayout(test_layout)
        
        # Comando personalizado
        custom_group = QGroupBox("⌨️ Comando Personalizado")
        custom_layout = QVBoxLayout(custom_group)
        
        self.custom_command = QTextEdit()
        self.custom_command.setMaximumHeight(80)
        self.custom_command.setPlainText("print('Hello from Pico!')")
        custom_layout.addWidget(self.custom_command)
        
        send_custom_btn = QPushButton("📤 Enviar Comando")
        send_custom_btn.clicked.connect(self.send_custom_command)
        custom_layout.addWidget(send_custom_btn)
        
        commands_layout.addWidget(custom_group)
        layout.addWidget(commands_group)
        
        layout.addStretch()
        return widget
        
    def apply_style(self):
        """Aplica estilos"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px 10px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #cce7ff;
            }
        """)
    
    def check_existing_connection(self):
        """Verifica se já existe uma conexão ativa com o Pico"""
        if pico_manager.is_connected():
            port = pico_manager.get_port()
            self.connection_status.setText("🟢 Já Conectado")
            self.connection_details.setText(f"Conexão ativa em {port}")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            
            # Adicionar ao output
            if hasattr(self, 'pico_output'):
                self.pico_output.append(f"\n🟢 Conexão existente detectada em {port}\n")
            
            self.log_message.emit(f"✅ Conexão existente detectada em {port}")
        else:
            self.connection_status.setText("🔴 Desconectado")
            self.connection_details.setText("Aguardando conexão...")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
        
    def start_port_scanner(self):
        """Inicia escaneamento de portas"""
        if not SERIAL_AVAILABLE:
            self.detection_status.setText("⚠️ pyserial não disponível - Modo simulação")
        else:
            self.detection_status.setText("🔍 Escaneando portas...")
            
        self.port_scanner = PortScannerThread()
        self.port_scanner.ports_updated.connect(self.update_ports_list)
        self.port_scanner.start()
        
    @pyqtSlot(list)
    def update_ports_list(self, ports):
        """Atualiza lista de portas"""
        self.ports_list.clear()
        self.port_combo.clear()
        
        pico_count = 0
        for port_info in ports:
            # Criar item da lista
            item_text = f"{port_info['device']} - {port_info['description']}"
            if port_info['is_pico']:
                item_text += " 🥧"
                pico_count += 1
                
            item = QListWidgetItem(item_text)
            if port_info['is_pico']:
                item.setBackground(QColor(200, 255, 200))  # Verde claro para Picos
                
            self.ports_list.addItem(item)
            self.port_combo.addItem(port_info['device'])
            
        # Atualizar status
        if pico_count > 0:
            self.detection_status.setText(f"✅ {pico_count} Raspberry Pi Pico(s) detectado(s)")
            
            # Auto-conectar se habilitado
            if self.auto_connect_cb.isChecked() and not self.current_connection:
                pico_port = next((p['device'] for p in ports if p['is_pico']), None)
                if pico_port:
                    self.port_combo.setCurrentText(pico_port)
                    self.connect_to_pico()
        else:
            total_ports = len(ports)
            if total_ports > 0:
                self.detection_status.setText(f"📡 {total_ports} porta(s) encontrada(s) - Nenhum Pico detectado")
            else:
                self.detection_status.setText("❌ Nenhuma porta encontrada")
                
    def refresh_ports(self):
        """Atualiza lista manualmente"""
        self.detection_status.setText("🔍 Atualizando...")
        
    def connect_to_pico(self):
        """Conecta ao Pico usando o gerenciador global"""
        port = self.port_combo.currentText()
        if not port:
            QMessageBox.warning(self, "Erro", "Selecione uma porta para conectar")
            return
            
        baudrate = int(self.baudrate_combo.currentText())
        
        self.connection_status.setText("🟡 Conectando...")
        self.connection_details.setText(f"Tentando conectar em {port}...")
        self.connect_btn.setEnabled(False)
        
        # Usar gerenciador de conexão
        success, message = pico_manager.connect(port, baudrate)
        
        if success:
            self.connection_status.setText("🟢 Conectado")
            self.connection_details.setText(message)
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            
            # Emitir sinal para janela principal
            self.connection_changed.emit(True, port)
            self.log_message.emit(message)
            
            # Adicionar ao output
            self.pico_output.append(f"\n{message}\n")
        else:
            self.connection_status.setText("🔴 Falha na Conexão")
            self.connection_details.setText(message)
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            
            # Emitir sinal de erro
            self.log_message.emit(message)
            
            QMessageBox.warning(self, "Erro de Conexão", message)
        
    @pyqtSlot(bool, str, str)
    def on_connection_result(self, success, port, message):
        """Resultado da tentativa de conexão"""
        if success:
            self.connection_status.setText("🟢 Conectado")
            self.connection_details.setText(f"Conectado em {port} - {message}")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.current_connection = self.connection_thread
            
            # Emitir sinal para janela principal
            self.connection_changed.emit(True, port)
            self.log_message.emit(f"Conectado ao Pico em {port}")
            
            # Adicionar ao output
            self.pico_output.append(f"🟢 CONECTADO: {port}")
            self.pico_output.append(f"📋 {message}")
            
        else:
            self.connection_status.setText("🔴 Erro na Conexão")
            self.connection_details.setText(f"Falha: {message}")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            
            self.log_message.emit(f"Erro ao conectar: {message}")
            self.pico_output.append(f"🔴 ERRO: {message}")
            
    @pyqtSlot(str)
    def on_output_received(self, text):
        """Recebe saída do Pico"""
        self.pico_output.append(text.strip())
        
        if self.auto_scroll.isChecked():
            cursor = self.pico_output.textCursor()
            cursor.movePosition(cursor.End)
            self.pico_output.setTextCursor(cursor)
            
    def disconnect_from_pico(self):
        """Desconecta do Pico usando o gerenciador global"""
        success, message = pico_manager.disconnect()
        
        self.connection_status.setText("🔴 Desconectado")
        self.connection_details.setText(message)
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        
        # Emitir sinal para janela principal
        self.connection_changed.emit(False, "")
        self.log_message.emit(message)
        
        # Adicionar ao output
        self.pico_output.append(f"\n{message}\n")
        
    def send_test_command(self, command):
        """Envia comando de teste usando o gerenciador global"""
        if not pico_manager.is_connected():
            self.pico_output.append("❌ Não conectado!")
            return
            
        self.pico_output.append(f"\n� COMANDO: {command}")
        success, response = pico_manager.send_command(command)
        
        if success:
            self.pico_output.append(f"� RESPOSTA:\n{response}")
        else:
            self.pico_output.append(f"❌ ERRO: {response}")
            QMessageBox.warning(self, "Erro", "Não há conexão ativa com o Pico")
            
    def send_custom_command(self):
        """Envia comando personalizado"""
        command = self.custom_command.toPlainText().strip()
        if command:
            self.send_test_command(command)
        else:
            QMessageBox.warning(self, "Erro", "Digite um comando para enviar")
            
    def clear_output(self):
        """Limpa saída"""
        self.pico_output.clear()
        self.pico_output.append("📺 Monitor limpo")
        
    def save_log(self):
        """Salva log"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salvar Log", "pico_log.txt", "Text Files (*.txt)"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.pico_output.toPlainText())
                QMessageBox.information(self, "Sucesso", f"Log salvo em {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar: {str(e)}")
                
    def closeEvent(self, event):
        """Evento de fechamento"""
        # Parar scanner
        if self.port_scanner:
            self.port_scanner.stop()
            self.port_scanner.wait()
            
        # Manter conexão ativa mesmo após fechar o diálogo
        event.accept()
#!/usr/bin/env python3
"""
Versão Simplificada do Raspberry Pi Pico File Uploader
Interface básica para upload de arquivos para o Pico
"""

import sys
import os
import time
import threading
from typing import List, Optional

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    print("Erro: PyQt5 não está instalado.")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Erro: pyserial não está instalado.")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)


class SimplePicoUploader(QMainWindow):
    """Versão simplificada do uploader para Pico"""
    
    def __init__(self):
        super().__init__()
        self.serial_conn = None
        self.connected = False
        
        self.init_ui()
        
    def init_ui(self):
        """Inicializa interface simples"""
        self.setWindowTitle("Pico File Uploader - Versão Simples")
        self.setGeometry(200, 200, 800, 600)
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Área de conexão
        conn_group = QGroupBox("Conexão")
        conn_layout = QHBoxLayout(conn_group)
        
        conn_layout.addWidget(QLabel("Porta:"))
        self.port_combo = QComboBox()
        self.refresh_ports()
        conn_layout.addWidget(self.port_combo)
        
        refresh_btn = QPushButton("Atualizar")
        refresh_btn.clicked.connect(self.refresh_ports)
        conn_layout.addWidget(refresh_btn)
        
        self.connect_btn = QPushButton("Conectar")
        self.connect_btn.clicked.connect(self.toggle_connection)
        conn_layout.addWidget(self.connect_btn)
        
        self.status_label = QLabel("Desconectado")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        conn_layout.addWidget(self.status_label)
        
        layout.addWidget(conn_group)
        
        # Área de arquivos
        files_group = QGroupBox("Arquivos")
        files_layout = QVBoxLayout(files_group)
        
        # Botões de seleção
        btn_layout = QHBoxLayout()
        
        select_file_btn = QPushButton("Selecionar Arquivo .py")
        select_file_btn.clicked.connect(self.select_file)
        btn_layout.addWidget(select_file_btn)
        
        upload_btn = QPushButton("Upload para Pico")
        upload_btn.clicked.connect(self.upload_file)
        btn_layout.addWidget(upload_btn)
        
        files_layout.addLayout(btn_layout)
        
        # Lista de arquivos
        self.file_list = QListWidget()
        files_layout.addWidget(self.file_list)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        list_files_btn = QPushButton("Listar Arquivos do Pico")
        list_files_btn.clicked.connect(self.list_pico_files)
        action_layout.addWidget(list_files_btn)
        
        run_btn = QPushButton("Executar main.py")
        run_btn.clicked.connect(self.run_main)
        action_layout.addWidget(run_btn)
        
        reset_btn = QPushButton("Reset Pico")
        reset_btn.clicked.connect(self.reset_pico)
        action_layout.addWidget(reset_btn)
        
        files_layout.addLayout(action_layout)
        
        layout.addWidget(files_group)
        
        # Console de log
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setFont(QFont("Courier", 9))
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        self.log("Aplicação iniciada. Conecte ao Raspberry Pi Pico para começar.")
    
    def log(self, message: str):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime("[%H:%M:%S] ")
        self.log_text.append(timestamp + message)
        # Auto scroll
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def refresh_ports(self):
        """Atualiza lista de portas seriais"""
        self.port_combo.clear()
        ports = []
        
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        
        if ports:
            self.port_combo.addItems(ports)
            self.log(f"Encontradas {len(ports)} portas seriais")
        else:
            self.port_combo.addItem("Nenhuma porta encontrada")
            self.log("Nenhuma porta serial encontrada")
    
    def toggle_connection(self):
        """Conecta/desconecta do Pico"""
        if not self.connected:
            port = self.port_combo.currentText()
            if "Nenhuma porta encontrada" in port:
                QMessageBox.warning(self, "Aviso", "Nenhuma porta disponível")
                return
            
            try:
                self.serial_conn = serial.Serial(port, 115200, timeout=1)
                time.sleep(0.1)
                
                # Testa conexão
                self.serial_conn.write(b'\x03')  # Ctrl+C
                time.sleep(0.1)
                self.serial_conn.write(b'\r\n')
                
                self.connected = True
                self.status_label.setText("Conectado")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.connect_btn.setText("Desconectar")
                self.log(f"Conectado em {port}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha na conexão: {e}")
                self.log(f"Erro na conexão: {e}")
        else:
            if self.serial_conn:
                self.serial_conn.close()
            
            self.connected = False
            self.status_label.setText("Desconectado")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.connect_btn.setText("Conectar")
            self.log("Desconectado")
    
    def select_file(self):
        """Seleciona arquivo Python para upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo Python",
            "",
            "Arquivos Python (*.py);;Todos os arquivos (*)"
        )
        
        if file_path:
            self.file_list.addItem(file_path)
            self.log(f"Arquivo selecionado: {os.path.basename(file_path)}")
    
    def upload_file(self):
        """Faz upload do arquivo selecionado"""
        if not self.connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        current_item = self.file_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo primeiro")
            return
        
        file_path = current_item.text()
        
        try:
            # Lê o arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(file_path)
            
            # Prepara comando de upload
            self.log(f"Iniciando upload de {filename}...")
            
            # Limpa buffer
            self.serial_conn.reset_input_buffer()
            
            # Comando para criar arquivo
            cmd = f"with open('{filename}', 'w') as f:\n"
            cmd += f"    f.write({repr(content)})\n"
            
            # Envia comando
            self.serial_conn.write(cmd.encode() + b'\r\n')
            time.sleep(0.5)
            
            # Verifica resposta
            response = ""
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
            
            if "Error" not in response and "Traceback" not in response:
                self.log(f"Upload de {filename} concluído com sucesso!")
                QMessageBox.information(self, "Sucesso", f"Arquivo {filename} enviado!")
            else:
                self.log(f"Erro no upload: {response}")
                QMessageBox.warning(self, "Erro", f"Falha no upload: {response}")
                
        except Exception as e:
            self.log(f"Erro no upload: {e}")
            QMessageBox.critical(self, "Erro", f"Erro no upload: {e}")
    
    def list_pico_files(self):
        """Lista arquivos no Pico"""
        if not self.connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        try:
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(b"import os; print(os.listdir())\r\n")
            time.sleep(0.5)
            
            response = ""
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
            
            self.log("Arquivos no Pico:")
            self.log(response)
            
        except Exception as e:
            self.log(f"Erro ao listar arquivos: {e}")
    
    def run_main(self):
        """Executa main.py no Pico"""
        if not self.connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        try:
            self.log("Executando main.py...")
            self.serial_conn.write(b"exec(open('main.py').read())\r\n")
            time.sleep(0.5)
            
            response = ""
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore')
            
            if response:
                self.log(f"Saída: {response}")
                
        except Exception as e:
            self.log(f"Erro ao executar: {e}")
    
    def reset_pico(self):
        """Reseta o Pico"""
        if not self.connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        try:
            self.log("Resetando Pico...")
            self.serial_conn.write(b"import machine; machine.reset()\r\n")
            
        except Exception as e:
            self.log(f"Erro no reset: {e}")
    
    def closeEvent(self, event):
        """Fecha aplicação"""
        if self.connected and self.serial_conn:
            self.serial_conn.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Pico Uploader Simples")
    
    window = SimplePicoUploader()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
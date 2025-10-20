#!/usr/bin/env python3
"""
Raspberry Pi Pico File Uploader - Interface PyQt5
Aplicação para conectar e fazer upload de arquivos para Raspberry Pi Pico
Similar à funcionalidade da extensão VS Code para Pico
"""

import sys
import os
import time
import threading
from pathlib import Path
from typing import List, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTextEdit, QComboBox, QLabel,
    QFileDialog, QMessageBox, QProgressBar, QSplitter,
    QTreeWidget, QTreeWidgetItem, QMenuBar, QAction,
    QStatusBar, QGroupBox, QGridLayout
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap

import serial
import serial.tools.list_ports


class PicoConnection:
    """Classe para gerenciar a conexão com o Raspberry Pi Pico"""
    
    def __init__(self):
        self.serial_connection = None
        self.is_connected = False
        
    def list_ports(self) -> List[str]:
        """Lista todas as portas seriais disponíveis"""
        ports = []
        for port in serial.tools.list_ports.comports():
            # Procura por dispositivos que podem ser Pico
            if any(keyword in port.description.lower() for keyword in 
                   ['pico', 'usb serial', 'ch340', 'cp2102', 'ftdi']):
                ports.append(f"{port.device} - {port.description}")
            else:
                ports.append(port.device)
        return ports
    
    def connect(self, port: str, baudrate: int = 115200) -> bool:
        """Conecta ao Pico na porta especificada"""
        try:
            # Extrai apenas o nome da porta
            port_name = port.split(' - ')[0] if ' - ' in port else port
            
            self.serial_connection = serial.Serial(
                port=port_name,
                baudrate=baudrate,
                timeout=1,
                write_timeout=1
            )
            
            # Testa a conexão enviando Ctrl+C para interromper qualquer execução
            self.serial_connection.write(b'\x03')
            time.sleep(0.1)
            
            # Envia comando para verificar se está no REPL
            self.serial_connection.write(b'\r\n')
            time.sleep(0.2)
            
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do Pico"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.is_connected = False
    
    def send_command(self, command: str) -> str:
        """Envia comando para o Pico e retorna a resposta"""
        if not self.is_connected or not self.serial_connection:
            return "Erro: Não conectado"
        
        try:
            # Limpa buffer de entrada
            self.serial_connection.reset_input_buffer()
            
            # Envia comando
            self.serial_connection.write((command + '\r\n').encode())
            
            # Lê resposta
            response = ""
            start_time = time.time()
            while time.time() - start_time < 2:  # Timeout de 2 segundos
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.read(self.serial_connection.in_waiting)
                    response += data.decode('utf-8', errors='ignore')
                time.sleep(0.01)
            
            return response
            
        except Exception as e:
            return f"Erro: {e}"
    
    def upload_file(self, local_path: str, remote_path: str = None) -> bool:
        """Faz upload de um arquivo para o Pico"""
        if not self.is_connected:
            return False
        
        try:
            if remote_path is None:
                remote_path = os.path.basename(local_path)
            
            # Lê o arquivo local
            with open(local_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Prepara comando para criar arquivo no Pico
            upload_command = f"""
with open('{remote_path}', 'w') as f:
    f.write({repr(content)})
"""
            
            # Envia comando
            response = self.send_command(upload_command)
            
            # Verifica se houve erro
            if "Traceback" in response or "Error" in response:
                return False
            
            return True
            
        except Exception as e:
            print(f"Erro no upload: {e}")
            return False
    
    def list_files(self) -> List[str]:
        """Lista arquivos no Pico"""
        if not self.is_connected:
            return []
        
        try:
            response = self.send_command("import os; print(os.listdir())")
            
            # Extrai lista de arquivos da resposta
            files = []
            lines = response.split('\n')
            for line in lines:
                if '[' in line and ']' in line:
                    # Processa linha que contém a lista de arquivos
                    file_list_str = line.strip()
                    if file_list_str.startswith('[') and file_list_str.endswith(']'):
                        file_list_str = file_list_str[1:-1]  # Remove [ ]
                        files = [f.strip().strip("'\"") for f in file_list_str.split(',') if f.strip()]
                    break
            
            return files
            
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            return []
    
    def delete_file(self, filename: str) -> bool:
        """Deleta arquivo do Pico"""
        if not self.is_connected:
            return False
        
        try:
            response = self.send_command(f"import os; os.remove('{filename}')")
            return "Traceback" not in response and "Error" not in response
            
        except Exception as e:
            print(f"Erro ao deletar arquivo: {e}")
            return False


class FileUploadThread(QThread):
    """Thread para upload de arquivos sem bloquear a interface"""
    
    progress_updated = pyqtSignal(int)
    upload_finished = pyqtSignal(bool, str)
    
    def __init__(self, pico_connection, files_to_upload):
        super().__init__()
        self.pico_connection = pico_connection
        self.files_to_upload = files_to_upload
    
    def run(self):
        """Executa o upload em thread separada"""
        total_files = len(self.files_to_upload)
        
        for i, (local_path, remote_path) in enumerate(self.files_to_upload):
            try:
                success = self.pico_connection.upload_file(local_path, remote_path)
                if not success:
                    self.upload_finished.emit(False, f"Erro no upload de {local_path}")
                    return
                
                # Atualiza progresso
                progress = int(((i + 1) / total_files) * 100)
                self.progress_updated.emit(progress)
                
            except Exception as e:
                self.upload_finished.emit(False, f"Erro: {e}")
                return
        
        self.upload_finished.emit(True, "Upload concluído com sucesso!")


class PicoUploaderApp(QMainWindow):
    """Aplicação principal do Pico Uploader"""
    
    def __init__(self):
        super().__init__()
        self.pico_connection = PicoConnection()
        self.upload_thread = None
        
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Raspberry Pi Pico File Uploader")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Criar menu
        self.create_menu()
        
        # Área de conexão
        connection_group = self.create_connection_area()
        main_layout.addWidget(connection_group)
        
        # Splitter para dividir as áreas
        splitter = QSplitter(Qt.Horizontal)
        
        # Área de arquivos locais
        local_files_widget = self.create_local_files_area()
        splitter.addWidget(local_files_widget)
        
        # Área de arquivos do Pico
        pico_files_widget = self.create_pico_files_area()
        splitter.addWidget(pico_files_widget)
        
        main_layout.addWidget(splitter)
        
        # Área de console/log
        console_group = self.create_console_area()
        main_layout.addWidget(console_group)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Desconectado")
        
    def create_menu(self):
        """Cria o menu da aplicação"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu('Arquivo')
        
        upload_action = QAction('Upload Arquivo', self)
        upload_action.triggered.connect(self.upload_single_file)
        file_menu.addAction(upload_action)
        
        upload_folder_action = QAction('Upload Pasta', self)
        upload_folder_action.triggered.connect(self.upload_folder)
        file_menu.addAction(upload_folder_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Sair', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu('Ferramentas')
        
        repl_action = QAction('Abrir REPL', self)
        repl_action.triggered.connect(self.open_repl)
        tools_menu.addAction(repl_action)
        
        reset_action = QAction('Reset Pico', self)
        reset_action.triggered.connect(self.reset_pico)
        tools_menu.addAction(reset_action)
    
    def create_connection_area(self):
        """Cria a área de conexão"""
        group = QGroupBox("Conexão com Raspberry Pi Pico")
        layout = QGridLayout(group)
        
        # Combo box para portas
        layout.addWidget(QLabel("Porta:"), 0, 0)
        self.port_combo = QComboBox()
        self.refresh_ports()
        layout.addWidget(self.port_combo, 0, 1)
        
        # Botão refresh portas
        refresh_btn = QPushButton("Atualizar")
        refresh_btn.clicked.connect(self.refresh_ports)
        layout.addWidget(refresh_btn, 0, 2)
        
        # Botão conectar/desconectar
        self.connect_btn = QPushButton("Conectar")
        self.connect_btn.clicked.connect(self.toggle_connection)
        layout.addWidget(self.connect_btn, 0, 3)
        
        # Status da conexão
        self.connection_status = QLabel("Desconectado")
        self.connection_status.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.connection_status, 0, 4)
        
        return group
    
    def create_local_files_area(self):
        """Cria a área de arquivos locais"""
        group = QGroupBox("Arquivos Locais")
        layout = QVBoxLayout(group)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        select_file_btn = QPushButton("Selecionar Arquivo")
        select_file_btn.clicked.connect(self.select_local_file)
        buttons_layout.addWidget(select_file_btn)
        
        select_folder_btn = QPushButton("Selecionar Pasta")
        select_folder_btn.clicked.connect(self.select_local_folder)
        buttons_layout.addWidget(select_folder_btn)
        
        layout.addLayout(buttons_layout)
        
        # Lista de arquivos selecionados
        self.local_files_tree = QTreeWidget()
        self.local_files_tree.setHeaderLabels(["Arquivo", "Tamanho"])
        layout.addWidget(self.local_files_tree)
        
        # Botão upload
        self.upload_btn = QPushButton("Upload Selecionados")
        self.upload_btn.clicked.connect(self.upload_selected_files)
        self.upload_btn.setEnabled(False)
        layout.addWidget(self.upload_btn)
        
        return group
    
    def create_pico_files_area(self):
        """Cria a área de arquivos do Pico"""
        group = QGroupBox("Arquivos no Pico")
        layout = QVBoxLayout(group)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Atualizar Lista")
        refresh_btn.clicked.connect(self.refresh_pico_files)
        buttons_layout.addWidget(refresh_btn)
        
        delete_btn = QPushButton("Deletar Selecionado")
        delete_btn.clicked.connect(self.delete_pico_file)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        # Lista de arquivos no Pico
        self.pico_files_tree = QTreeWidget()
        self.pico_files_tree.setHeaderLabels(["Arquivo"])
        layout.addWidget(self.pico_files_tree)
        
        return group
    
    def create_console_area(self):
        """Cria a área do console"""
        group = QGroupBox("Console / Log")
        layout = QVBoxLayout(group)
        
        self.console_text = QTextEdit()
        self.console_text.setMaximumHeight(150)
        self.console_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.console_text)
        
        return group
    
    def setup_timer(self):
        """Configura timer para atualização automática"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(5000)  # Atualiza a cada 5 segundos
    
    def log_message(self, message: str):
        """Adiciona mensagem ao console"""
        timestamp = time.strftime("[%H:%M:%S] ")
        self.console_text.append(timestamp + message)
        self.console_text.verticalScrollBar().setValue(
            self.console_text.verticalScrollBar().maximum()
        )
    
    def refresh_ports(self):
        """Atualiza lista de portas disponíveis"""
        self.port_combo.clear()
        ports = self.pico_connection.list_ports()
        if ports:
            self.port_combo.addItems(ports)
        else:
            self.port_combo.addItem("Nenhuma porta encontrada")
        
        self.log_message(f"Encontradas {len(ports)} portas seriais")
    
    def toggle_connection(self):
        """Conecta ou desconecta do Pico"""
        if not self.pico_connection.is_connected:
            # Conectar
            port = self.port_combo.currentText()
            if "Nenhuma porta encontrada" in port:
                QMessageBox.warning(self, "Aviso", "Nenhuma porta disponível")
                return
            
            self.log_message(f"Tentando conectar em {port}...")
            
            if self.pico_connection.connect(port):
                self.connection_status.setText("Conectado")
                self.connection_status.setStyleSheet("color: green; font-weight: bold;")
                self.connect_btn.setText("Desconectar")
                self.upload_btn.setEnabled(True)
                self.status_bar.showMessage(f"Conectado em {port}")
                self.log_message("Conectado com sucesso!")
                self.refresh_pico_files()
            else:
                QMessageBox.critical(self, "Erro", "Falha na conexão com o Pico")
                self.log_message("Falha na conexão")
        else:
            # Desconectar
            self.pico_connection.disconnect()
            self.connection_status.setText("Desconectado")
            self.connection_status.setStyleSheet("color: red; font-weight: bold;")
            self.connect_btn.setText("Conectar")
            self.upload_btn.setEnabled(False)
            self.status_bar.showMessage("Desconectado")
            self.log_message("Desconectado")
    
    def select_local_file(self):
        """Seleciona arquivo local para upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar Arquivo Python", 
            "", 
            "Arquivos Python (*.py);;Todos os arquivos (*)"
        )
        
        if file_path:
            self.add_local_file(file_path)
    
    def select_local_folder(self):
        """Seleciona pasta local para upload"""
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        
        if folder_path:
            # Adiciona todos os arquivos .py da pasta
            for file_path in Path(folder_path).glob("**/*.py"):
                self.add_local_file(str(file_path))
    
    def add_local_file(self, file_path: str):
        """Adiciona arquivo à lista de arquivos locais"""
        file_size = os.path.getsize(file_path)
        size_str = f"{file_size} bytes"
        
        item = QTreeWidgetItem([os.path.basename(file_path), size_str])
        item.setData(0, Qt.UserRole, file_path)  # Armazena caminho completo
        self.local_files_tree.addTopLevelItem(item)
        
        self.log_message(f"Arquivo adicionado: {os.path.basename(file_path)}")
    
    def upload_selected_files(self):
        """Faz upload dos arquivos selecionados"""
        if not self.pico_connection.is_connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        # Coleta arquivos para upload
        files_to_upload = []
        root = self.local_files_tree.invisibleRootItem()
        
        for i in range(root.childCount()):
            item = root.child(i)
            local_path = item.data(0, Qt.UserRole)
            remote_path = item.text(0)  # Nome do arquivo
            files_to_upload.append((local_path, remote_path))
        
        if not files_to_upload:
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo selecionado")
            return
        
        # Inicia upload em thread separada
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.upload_thread = FileUploadThread(self.pico_connection, files_to_upload)
        self.upload_thread.progress_updated.connect(self.progress_bar.setValue)
        self.upload_thread.upload_finished.connect(self.on_upload_finished)
        self.upload_thread.start()
        
        self.log_message(f"Iniciando upload de {len(files_to_upload)} arquivo(s)...")
    
    def on_upload_finished(self, success: bool, message: str):
        """Callback quando upload termina"""
        self.progress_bar.setVisible(False)
        
        if success:
            self.log_message(message)
            QMessageBox.information(self, "Sucesso", message)
            # Limpa lista de arquivos locais
            self.local_files_tree.clear()
            # Atualiza lista do Pico
            self.refresh_pico_files()
        else:
            self.log_message(f"Erro: {message}")
            QMessageBox.critical(self, "Erro", message)
    
    def refresh_pico_files(self):
        """Atualiza lista de arquivos no Pico"""
        if not self.pico_connection.is_connected:
            return
        
        self.pico_files_tree.clear()
        files = self.pico_connection.list_files()
        
        for filename in files:
            item = QTreeWidgetItem([filename])
            self.pico_files_tree.addTopLevelItem(item)
        
        self.log_message(f"Encontrados {len(files)} arquivos no Pico")
    
    def delete_pico_file(self):
        """Deleta arquivo selecionado do Pico"""
        current_item = self.pico_files_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo para deletar")
            return
        
        filename = current_item.text(0)
        
        reply = QMessageBox.question(
            self, 
            "Confirmar", 
            f"Deletar arquivo '{filename}' do Pico?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.pico_connection.delete_file(filename):
                self.log_message(f"Arquivo '{filename}' deletado")
                self.refresh_pico_files()
            else:
                QMessageBox.critical(self, "Erro", f"Falha ao deletar '{filename}'")
    
    def upload_single_file(self):
        """Upload de arquivo único via menu"""
        self.select_local_file()
        if self.local_files_tree.topLevelItemCount() > 0:
            self.upload_selected_files()
    
    def upload_folder(self):
        """Upload de pasta via menu"""
        self.select_local_folder()
        if self.local_files_tree.topLevelItemCount() > 0:
            self.upload_selected_files()
    
    def open_repl(self):
        """Abre REPL do Pico"""
        if not self.pico_connection.is_connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        # Implementar janela REPL separada aqui se necessário
        self.log_message("REPL: Use o terminal MicroPython para interação direta")
    
    def reset_pico(self):
        """Reseta o Pico"""
        if not self.pico_connection.is_connected:
            QMessageBox.warning(self, "Aviso", "Conecte ao Pico primeiro")
            return
        
        response = self.pico_connection.send_command("import machine; machine.reset()")
        self.log_message("Comando de reset enviado")
    
    def auto_refresh(self):
        """Atualização automática periódica"""
        if self.pico_connection.is_connected:
            # Atualiza lista de arquivos do Pico automaticamente
            pass  # Desabilitado para evitar spam
    
    def closeEvent(self, event):
        """Evento de fechamento da aplicação"""
        if self.pico_connection.is_connected:
            self.pico_connection.disconnect()
        
        if self.upload_thread and self.upload_thread.isRunning():
            self.upload_thread.quit()
            self.upload_thread.wait()
        
        event.accept()


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    app.setApplicationName("Pico Uploader")
    
    # Verifica se as dependências estão instaladas
    try:
        import serial
    except ImportError:
        QMessageBox.critical(
            None, 
            "Erro de Dependência", 
            "Biblioteca 'pyserial' não encontrada.\n"
            "Instale com: pip install pyserial"
        )
        sys.exit(1)
    
    window = PicoUploaderApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
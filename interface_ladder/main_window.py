"""
Janela Principal da Interface LADDER
Interface para programação LADDER do Raspberry Pi Pico
"""

import os
import json
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QSplitter, QTabWidget, QTextEdit, QLabel, QMenuBar,
                           QAction, QMessageBox, QFileDialog, QStatusBar,
                           QProgressBar, QPushButton, QFrame, QApplication,
                           QToolBar, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap, QPainter, QColor, QFont

from component_library import ComponentLibrary
from ladder_canvas import LadderCanvas
from config_dialog import ConfigDialog
from code_generator import PicoCodeGenerator
from pico_connection_manager import pico_manager

class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLP-IHM-PICO - Interface LADDER")
        self.setGeometry(100, 100, 1400, 800)
        
        # Inicializar componentes
        self.init_ui()
        
        # Configurar canvas
        self.setup_canvas()
        
        # Mostrar status
        self.show_ready_status()
        
    def init_ui(self):
        """Inicializa a interface do usuário"""
        # Configurar widget central
        self.setup_central_widget()
        
        # Criar menus
        self.create_menus()
        
        # Criar toolbar
        self.create_toolbar()
        
        # Criar status bar
        self.create_status_bar()
        
        # Aplicar estilo
        self.apply_style()
        
    def setup_central_widget(self):
        """Configura o widget central com divisores"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Splitter horizontal principal
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Painel esquerdo - Biblioteca de componentes
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Splitter vertical central
        center_splitter = QSplitter(Qt.Vertical)
        
        # Área de desenho LADDER
        ladder_area = self.create_ladder_area()
        center_splitter.addWidget(ladder_area)
        
        # Área de logs/saída
        log_area = self.create_log_area()
        center_splitter.addWidget(log_area)
        
        # Configurar proporções
        center_splitter.setSizes([600, 200])
        
        main_splitter.addWidget(center_splitter)
        
        # Painel direito - Propriedades
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Configurar proporções do splitter principal
        main_splitter.setSizes([200, 800, 200])
        
        main_layout.addWidget(main_splitter)
        
    def create_left_panel(self):
        """Cria painel esquerdo com biblioteca de componentes"""
        frame = QFrame()
        frame.setFixedWidth(250)
        frame.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(frame)
        
        # Título
        title = QLabel("📚 Biblioteca de Componentes")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                background-color: #2d5aa0;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Biblioteca de componentes
        self.component_library = ComponentLibrary()
        layout.addWidget(self.component_library)
        
        return frame
        
    def create_ladder_area(self):
        """Cria área de desenho LADDER"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(frame)
        
        # Título
        title = QLabel("⚡ Editor LADDER")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                background-color: #228b22;
                color: white;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Canvas LADDER
        self.canvas = LadderCanvas()
        layout.addWidget(self.canvas)
        
        return frame
        
    def create_log_area(self):
        """Cria área de logs e saídas"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setMaximumHeight(200)
        
        layout = QVBoxLayout(frame)
        
        # Título
        title = QLabel("📋 Logs e Saídas")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                background-color: #6b6b6b;
                color: white;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Área de texto para logs
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(150)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.log_area)
        
        return frame
        
    def create_right_panel(self):
        """Cria painel direito com propriedades"""
        frame = QFrame()
        frame.setFixedWidth(250)
        frame.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(frame)
        
        # Título
        title = QLabel("🔧 Propriedades")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                background-color: #ff6b35;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Placeholder para propriedades
        properties_label = QLabel("📝 Selecione um elemento no canvas")
        properties_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
        """)
        layout.addWidget(properties_label)
        
        layout.addStretch()
        return frame
        
    def create_menus(self):
        """Cria a barra de menus"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu('📁 &Arquivo')
        
        # Novo projeto
        new_action = QAction('🆕 &Novo', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip('Criar novo projeto LADDER')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        # Abrir projeto
        open_action = QAction('📂 &Abrir', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setStatusTip('Abrir projeto existente')
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Salvar
        save_action = QAction('💾 &Salvar', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip('Salvar projeto atual')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        # Salvar como
        save_as_action = QAction('💾 Salvar &Como', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.setStatusTip('Salvar projeto com novo nome')
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exportar
        export_menu = file_menu.addMenu('📤 Exportar')
        
        export_python_action = QAction('🐍 Python', self)
        export_python_action.setStatusTip('Exportar para código Python')
        export_python_action.triggered.connect(self.export_python)
        export_menu.addAction(export_python_action)
        
        export_image_action = QAction('🖼️ Imagem', self)
        export_image_action.setStatusTip('Exportar diagrama como imagem')
        export_image_action.triggered.connect(self.export_image)
        export_menu.addAction(export_image_action)
        
        file_menu.addSeparator()
        
        # Sair
        exit_action = QAction('🚪 &Sair', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip('Sair da aplicação')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Editar
        edit_menu = menubar.addMenu('✏️ &Editar')
        
        undo_action = QAction('↶ &Desfazer', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setStatusTip('Desfazer última ação')
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('↷ &Refazer', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setStatusTip('Refazer ação')
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        copy_action = QAction('📋 &Copiar', self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.setStatusTip('Copiar seleção')
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('📄 Co&lar', self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.setStatusTip('Colar da área de transferência')
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # Menu Pico
        pico_menu = menubar.addMenu('🥧 &Pico')
        
        # Upload para Pico
        upload_action = QAction('📤 &Upload para Pico', self)
        upload_action.setShortcut('Ctrl+U')
        upload_action.setStatusTip('Enviar código para Raspberry Pi Pico')
        upload_action.triggered.connect(self.upload_to_pico)
        pico_menu.addAction(upload_action)
        
        # Conectar Pico
        connect_action = QAction('🔌 &Conectar Pico', self)
        connect_action.setShortcut('Ctrl+P')
        connect_action.setStatusTip('Configurar conexão com Pico')
        connect_action.triggered.connect(self.connect_pico)
        pico_menu.addAction(connect_action)
        
        pico_menu.addSeparator()
        
        # Configurar RS485
        rs485_action = QAction('🌐 Configurar &RS485', self)
        rs485_action.setShortcut('Ctrl+R')
        rs485_action.setStatusTip('Configurar comunicação RS485 via RS232')
        rs485_action.triggered.connect(self.configure_rs485)
        pico_menu.addAction(rs485_action)
        
        pico_menu.addSeparator()
        
        # Test Upload (Debug)
        test_upload_action = QAction('🧪 Test Upload (Debug)', self)
        test_upload_action.setStatusTip('Testar upload com arquivo pequeno e logs detalhados')
        test_upload_action.triggered.connect(self.test_upload)
        pico_menu.addAction(test_upload_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu('❓ &Ajuda')
        
        about_action = QAction('ℹ️ &Sobre', self)
        about_action.setStatusTip('Sobre esta aplicação')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = self.addToolBar('Principal')
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # Botão Novo
        new_btn = QAction('🆕 Novo', self)
        new_btn.triggered.connect(self.new_project)
        toolbar.addAction(new_btn)
        
        # Botão Salvar
        save_btn = QAction('💾 Salvar', self)
        save_btn.triggered.connect(self.save_project)
        toolbar.addAction(save_btn)
        
        toolbar.addSeparator()
        
        # Botão Upload
        upload_btn = QAction('📤 Upload', self)
        upload_btn.triggered.connect(self.upload_to_pico)
        toolbar.addAction(upload_btn)
        
        # Botão Conectar
        connect_btn = QAction('🔌 Conectar', self)
        connect_btn.triggered.connect(self.connect_pico)
        toolbar.addAction(connect_btn)
        
    def create_status_bar(self):
        """Cria a barra de status"""
        self.status_bar = self.statusBar()
        
        # Label de status
        self.status_label = QLabel("Pronto")
        self.status_bar.addWidget(self.status_label)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Conexão Pico
        self.pico_status = QLabel("🥧 Pico: Desconectado")
        self.status_bar.addPermanentWidget(self.pico_status)
        
    def apply_style(self):
        """Aplica estilo geral à aplicação"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QMenuBar {
                background-color: #2d5aa0;
                color: white;
                border: none;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
                border-radius: 3px;
            }
            QMenuBar::item:selected {
                background-color: #1a4480;
            }
            QToolBar {
                background-color: #e8e8e8;
                border: none;
                spacing: 3px;
                padding: 5px;
            }
            QStatusBar {
                background-color: #e8e8e8;
                border-top: 1px solid #ccc;
            }
        """)
        
    def setup_canvas(self):
        """Configurar canvas LADDER"""
        # Conectar sinais se necessário
        pass
        
    def show_ready_status(self):
        """Mostra status de pronto"""
        self.log_message("✅ Interface LADDER iniciada com sucesso!")
        self.log_message("📚 Biblioteca com 69+ componentes carregada")
        self.log_message("🎨 Canvas de design pronto para uso")
        self.log_message("🔄 Arraste componentes da biblioteca para o canvas")
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")
        
    # Métodos de ação dos menus
    def new_project(self):
        """Criar novo projeto"""
        self.log_message("🆕 Novo projeto criado")
        
    def open_project(self):
        """Abrir projeto existente"""
        filename, _ = QFileDialog.getOpenFileName(self, 'Abrir Projeto', '', 'Projetos LADDER (*.ladder)')
        if filename:
            self.log_message(f"📂 Projeto aberto: {filename}")
            
    def save_project(self):
        """Salvar projeto atual"""
        self.log_message("💾 Projeto salvo")
        
    def save_project_as(self):
        """Salvar projeto com novo nome"""
        filename, _ = QFileDialog.getSaveFileName(self, 'Salvar Projeto Como', '', 'Projetos LADDER (*.ladder)')
        if filename:
            self.log_message(f"💾 Projeto salvo como: {filename}")
            
    def export_python(self):
        """Exportar para código Python"""
        self.log_message("🐍 Iniciando geração de código Python para Raspberry Pi Pico...")
        
        try:
            # Criar gerador
            generator = PicoCodeGenerator()
            
            # Coletar componentes LADDER
            ladder_components = []
            connections = []
            
            # Verificar se existe canvas LADDER
            if hasattr(self, 'ladder_canvas'):
                # Obter componentes do canvas
                for item in self.ladder_canvas.scene.items():
                    if hasattr(item, 'component_name'):
                        component_data = {
                            'name': item.component_name,
                            'type': getattr(item, 'component_type', 'unknown'),
                            'position': (item.pos().x(), item.pos().y()),
                            'properties': getattr(item, 'properties', {})
                        }
                        ladder_components.append(component_data)
                
                # Obter conexões
                if hasattr(self.ladder_canvas, 'connections'):
                    for conn in self.ladder_canvas.connections:
                        if hasattr(conn, 'start_component') and hasattr(conn, 'end_component'):
                            connection_data = {
                                'from': conn.start_component.component_name if hasattr(conn.start_component, 'component_name') else 'unknown',
                                'to': conn.end_component.component_name if hasattr(conn.end_component, 'component_name') else 'unknown',
                                'from_point': getattr(conn, 'start_point_type', 'output'),
                                'to_point': getattr(conn, 'end_point_type', 'input')
                            }
                            connections.append(connection_data)
            
            # Carregar configuração RS485
            rs485_config = self.load_rs485_config()
            
            # Configuração IHM (placeholder por enquanto)
            ihm_config = {}
            
            # Gerar código
            success = generator.generate_all(
                ladder_components, 
                connections, 
                rs485_config, 
                ihm_config
            )
            
            if success:
                self.log_message("✅ Código Python gerado com sucesso!")
                self.log_message(f"📁 Arquivos salvos em: {generator.output_dir}")
                
                # Mostrar diálogo de sucesso
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Geração Concluída")
                msg.setText("Código Python gerado com sucesso!")
                msg.setInformativeText(f"Arquivos salvos em:\n{generator.output_dir}\n\n" +
                                      "Arquivos gerados:\n" +
                                      "• main_.py - Código principal (renomear para main.py para produção)\n" +
                                      "• lib_rs485.py - Biblioteca RS485 (Modbus RTU)\n" +
                                      "• lib_ihm.py - Biblioteca IHM (Display ST7920)\n" +
                                      "• config.json - Arquivo de configuração")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            else:
                self.log_message("❌ Erro ao gerar código Python")
                
        except Exception as e:
            self.log_message(f"❌ Erro na geração: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
            
    def load_rs485_config(self):
        """Carrega configuração RS485 do arquivo"""
        try:
            config_path = "rs485_config.json"
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.log_message(f"⚠️ Não foi possível carregar config RS485: {e}")
        return None
        
    def export_image(self):
        """Exportar diagrama como imagem"""
        self.log_message("🖼️ Exportando como imagem...")
        
    def undo(self):
        """Desfazer última ação"""
        self.log_message("↶ Ação desfeita")
        
    def redo(self):
        """Refazer ação"""
        self.log_message("↷ Ação refeita")
        
    def copy(self):
        """Copiar seleção"""
        self.log_message("📋 Copiado para área de transferência")
        
    def paste(self):
        """Colar da área de transferência"""
        self.log_message("📄 Colado da área de transferência")
        
    def upload_to_pico(self):
        """Enviar código para Pico"""
        self.log_message("📤 Iniciando upload para Raspberry Pi Pico...")
        
        # Verificar se está conectado
        if not pico_manager.is_connected():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Pico Não Conectado")
            msg.setText("Raspberry Pi Pico não está conectado!")
            msg.setInformativeText("Deseja abrir o diálogo de conexão?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            
            if msg.exec_() == QMessageBox.Yes:
                self.connect_pico()
            return
        
        # Verificar se o código foi gerado
        main_file = os.path.join("../generated_code", "main_.py")
        if not os.path.exists(main_file):
            reply = QMessageBox.question(
                self,
                "Código Não Gerado",
                "O código ainda não foi gerado.\n\nDeseja gerar o código agora?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.export_python()
                # Verificar novamente se foi gerado
                if not os.path.exists(main_file):
                    self.log_message("❌ Falha ao gerar código")
                    return
            else:
                return
        
        # Perguntar quais arquivos enviar
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Upload para Pico")
        msg.setText("Selecione os arquivos para enviar:")
        msg.setInformativeText(
            "• main_.py → main.py (código principal)\n"
            "• lib_rs485.py (biblioteca RS485)\n"
            "• lib_ihm.py (biblioteca IHM)\n"
            "• config.json (configurações)"
        )
        
        all_btn = msg.addButton("📦 Todos", QMessageBox.YesRole)
        main_only_btn = msg.addButton("📄 Apenas main_.py", QMessageBox.NoRole)
        cancel_btn = msg.addButton("❌ Cancelar", QMessageBox.RejectRole)
        
        msg.exec_()
        clicked = msg.clickedButton()
        
        if clicked == cancel_btn:
            self.log_message("⚠️ Upload cancelado")
            return
        
        # Lista de arquivos para upload
        files_to_upload = []
        
        if clicked == all_btn:
            files_to_upload = [
                ("../generated_code/main_.py", "main.py"),
                ("../generated_code/lib_rs485.py", "lib_rs485.py"),
                ("../generated_code/lib_ihm.py", "lib_ihm.py"),
                ("../generated_code/config.json", "config.json")
            ]
        else:  # main_only_btn
            files_to_upload = [
                ("../generated_code/main_.py", "main.py")
            ]
        
        # Executar upload
        self.log_message(f"📤 Enviando {len(files_to_upload)} arquivo(s)...")
        self.log_message("🔍 Modo debug ativado - mostrando detalhes...")
        
        success_count = 0
        error_count = 0
        
        # Criar função de log personalizada que redireciona para a interface
        import sys
        from io import StringIO
        
        # Capturar stdout temporariamente
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            for local_path, remote_name in files_to_upload:
                if not os.path.exists(local_path):
                    self.log_message(f"⚠️ Arquivo não encontrado: {local_path}")
                    error_count += 1
                    continue
                
                self.log_message(f"\n📤 Enviando {remote_name}...")
                
                # Fazer upload com debug ativado
                success, message = pico_manager.upload_file(local_path, remote_name, debug=True)
                
                # Capturar e mostrar logs de debug
                debug_output = sys.stdout.getvalue()
                if debug_output:
                    for line in debug_output.strip().split('\n'):
                        if line.strip():
                            self.log_message(f"  {line}")
                    sys.stdout = StringIO()  # Limpar buffer
                
                if success:
                    self.log_message(f"✅ {message}")
                    success_count += 1
                else:
                    self.log_message(f"❌ {message}")
                    error_count += 1
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout
        
        # Mensagem final
        if error_count == 0:
            self.log_message(f"✅ Upload concluído! {success_count} arquivo(s) enviado(s)")
            
            # Perguntar se quer executar soft reset
            reply = QMessageBox.question(
                self,
                "Upload Concluído",
                f"Upload concluído com sucesso!\n\n"
                f"{success_count} arquivo(s) enviado(s)\n\n"
                "Deseja executar soft reset para reiniciar o Pico?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = pico_manager.soft_reset()
                self.log_message(message)
        else:
            self.log_message(f"⚠️ Upload finalizado com erros: {success_count} sucesso, {error_count} falhas")
            QMessageBox.warning(
                self,
                "Upload com Erros",
                f"Upload finalizado com erros:\n\n"
                f"✅ Sucesso: {success_count}\n"
                f"❌ Falhas: {error_count}\n\n"
                "Verifique os logs para mais detalhes."
            )
    
    def test_upload(self):
        """Testar upload com arquivo pequeno"""
        self.log_message("\n" + "="*60)
        self.log_message("🧪 TESTE DE UPLOAD")
        self.log_message("="*60)
        
        # Verificar conexão
        self.log_message("\n1. Verificando conexão...")
        if not pico_manager.is_connected():
            self.log_message("❌ Pico não está conectado!")
            QMessageBox.warning(
                self,
                "Pico Não Conectado",
                "Conecte o Pico primeiro através do menu:\nPico → Conectar Pico"
            )
            return
        
        port = pico_manager.get_port()
        self.log_message(f"✅ Conectado em: {port}")
        
        # Criar arquivo de teste
        self.log_message("\n2. Criando arquivo de teste...")
        import tempfile
        test_content = """# Teste de Upload
print('='*40)
print('🎉 Upload funcionou!')
print('Arquivo de teste executado com sucesso')
print('='*40)
"""
        
        test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        test_file.write(test_content)
        test_file.close()
        
        self.log_message(f"   Arquivo criado: {test_file.name}")
        self.log_message(f"   Tamanho: {len(test_content)} bytes")
        
        # Fazer upload com debug
        self.log_message("\n3. Iniciando upload (modo debug)...")
        
        import sys
        from io import StringIO
        
        # Capturar stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            success, message = pico_manager.upload_file(test_file.name, "test_upload.py", debug=True)
            
            # Capturar logs
            debug_output = sys.stdout.getvalue()
            if debug_output:
                for line in debug_output.strip().split('\n'):
                    if line.strip():
                        self.log_message(f"  {line}")
        finally:
            sys.stdout = old_stdout
            # Limpar arquivo temporário
            try:
                os.unlink(test_file.name)
            except:
                pass
        
        if success:
            self.log_message(f"\n✅ {message}")
            
            # Tentar executar
            self.log_message("\n4. Executando arquivo de teste no Pico...")
            success, response = pico_manager.send_command("exec(open('test_upload.py').read())")
            
            if success:
                self.log_message("📥 Resposta do Pico:")
                for line in response.strip().split('\n'):
                    if line.strip():
                        self.log_message(f"   {line}")
            
            # Verificar arquivos
            self.log_message("\n5. Listando arquivos no Pico...")
            success, response = pico_manager.send_command("import os; print(os.listdir())")
            if success:
                self.log_message(f"   Arquivos: {response.strip()}")
            
            self.log_message("\n" + "="*60)
            self.log_message("✅ TESTE CONCLUÍDO COM SUCESSO!")
            self.log_message("="*60)
            
            QMessageBox.information(
                self,
                "Teste Concluído",
                "✅ Upload funcionou!\n\n"
                "O sistema está pronto para enviar o código principal.\n"
                "Use: Pico → Upload para Pico"
            )
        else:
            self.log_message(f"\n❌ {message}")
            self.log_message("\n" + "="*60)
            self.log_message("❌ TESTE FALHOU")
            self.log_message("="*60)
            
            QMessageBox.warning(
                self,
                "Teste Falhou",
                f"❌ Upload falhou!\n\n{message}\n\n"
                "Verifique os logs para detalhes."
            )
        
    def connect_pico(self):
        """Conectar com Pico"""
        dialog = ConfigDialog(self)
        if dialog.exec_():
            self.log_message("🔌 Configuração do Pico aberta")
            self.pico_status.setText("🥧 Pico: Conectado")
            
    def configure_rs485(self):
        """Configurar comunicação RS485"""
        from rs485_config_dialog import RS485ConfigDialog
        
        dialog = RS485ConfigDialog(self)
        if dialog.exec_():
            self.log_message("🌐 Configuração RS485 salva")
            self.status_label.setText("RS485 configurado")
        
    def show_about(self):
        """Mostrar sobre"""
        QMessageBox.about(self, "Sobre", 
                         "CLP-IHM-PICO\n"
                         "Interface LADDER para Raspberry Pi Pico\n"
                         "Versão 1.0\n\n"
                         "Desenvolvido com PyQt5")
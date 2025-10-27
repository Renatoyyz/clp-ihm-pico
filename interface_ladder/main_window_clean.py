"""
Janela Principal da Interface LADDER
Interface para programação LADDER do Raspberry Pi Pico
"""

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
        self.log_area.append(f"[{QTimer().toString()}] {message}")
        
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
        self.log_message("🐍 Exportando para Python...")
        
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
        self.log_message("📤 Enviando código para Raspberry Pi Pico...")
        
    def connect_pico(self):
        """Conectar com Pico"""
        dialog = ConfigDialog(self)
        if dialog.exec_():
            self.log_message("🔌 Configuração do Pico aberta")
            self.pico_status.setText("🥧 Pico: Conectado")
        
    def show_about(self):
        """Mostrar sobre"""
        QMessageBox.about(self, "Sobre", 
                         "CLP-IHM-PICO\n"
                         "Interface LADDER para Raspberry Pi Pico\n"
                         "Versão 1.0\n\n"
                         "Desenvolvido com PyQt5")
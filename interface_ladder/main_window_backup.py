#!/usr/bin/env python3
"""
Interface LADDER - Janela Principal
Sistema de programação visual para Raspberry Pi Pico
"""

import sys
import os
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

# Importar módulos da aplicação
from config_dialog import ConfigDialog
from component_library import ComponentLibrary
from ladder_canvas import LadderCanvas


class MainWindow(QMainWindow):
    """Janela principal da aplicação LADDER"""
    
    def __init__(self):
        super().__init__()
        self.config_dialog = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("CLP-IHM-PICO - Interface LADDER")
        self.setGeometry(100, 100, 1200, 800)
        
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
        
    def create_ladder_tab(self):
        """Cria aba para programação LADDER"""
        ladder_widget = QWidget()
        
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
        
        layout = QVBoxLayout(ladder_widget)
        layout.addWidget(main_splitter)
        
        # Adicionar aba LADDER
        self.tabs.addTab(ladder_widget, "⚡ LADDER")
        
    def create_left_panel(self):
        """Cria painel esquerdo com biblioteca de componentes"""
        # Usar a nova ComponentLibrary
        self.component_library = ComponentLibrary()
        self.component_library.setMinimumWidth(220)
        self.component_library.setMaximumWidth(300)
        
        return self.component_library
        
    def create_ladder_area(self):
        """Cria área principal de desenho LADDER"""
        # Usar o novo LadderCanvas
        self.ladder_canvas = LadderCanvas()
        
        # Configurar componentes canvas
        self.setup_canvas_components()
        
    def setup_canvas_components(self):
        """Configurar componentes do canvas LADDER"""
        # Conectar sinais do canvas LADDER se existir
        if hasattr(self, 'canvas'):
            pass  # Aqui colocaremos sinais do canvas LADDER quando necessário

    def create_ihm_tab(self):
        """Cria aba para design de IHM"""
        # Criar widget principal da aba IHM
        ihm_widget = QWidget()
        ihm_layout = QHBoxLayout(ihm_widget)
        ihm_layout.setContentsMargins(5, 5, 5, 5)
        
        # Painel esquerdo - Gerenciador de telas e biblioteca
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(2, 2, 2, 2)
        
        # Gerenciador de telas
        self.screen_manager = IHMScreenManager()
        left_layout.addWidget(self.screen_manager, 1)
        
        # Biblioteca de componentes IHM
        self.ihm_component_library = IHMComponentLibrary()
        left_layout.addWidget(self.ihm_component_library, 2)
        
        ihm_layout.addWidget(left_panel)
        
        # Painel central - Canvas de design
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(5, 5, 5, 5)
        
        # Título do canvas
        canvas_title = QLabel("📱 Design da Tela IHM (128x64)")
        canvas_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2d5aa0;
                padding: 8px;
                background-color: #f0f8ff;
                border: 1px solid #b8d4f0;
                border-radius: 4px;
                margin-bottom: 5px;
            }
        """)
        center_layout.addWidget(canvas_title)
        
        # Canvas IHM
        self.ihm_canvas = IHMScreenCanvas()
        center_layout.addWidget(self.ihm_canvas, 1)
        
        # Informações da tela atual
        self.screen_info_label = QLabel("Tela: Nenhuma selecionada")
        self.screen_info_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 3px;
                font-size: 11px;
            }
        """)
        center_layout.addWidget(self.screen_info_label)
        
        ihm_layout.addWidget(center_panel, 1)
        
        # Painel direito - Propriedades
        self.ihm_properties = IHMPropertiesPanel()
        self.ihm_properties.setFixedWidth(250)
        ihm_layout.addWidget(self.ihm_properties)
        
        # Adicionar aba IHM ao tab widget principal
        self.tabs.addTab(ihm_widget, "🖥️ IHM")
        """Cria aba para design de IHM"""
        # Criar widget principal da aba IHM
        ihm_widget = QWidget()
        ihm_layout = QHBoxLayout(ihm_widget)
        ihm_layout.setContentsMargins(5, 5, 5, 5)
        
        # Painel esquerdo - Gerenciador de telas e biblioteca
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(2, 2, 2, 2)
        
        # Gerenciador de telas
        self.screen_manager = IHMScreenManager()
        left_layout.addWidget(self.screen_manager, 1)
        
        # Biblioteca de componentes IHM
        self.ihm_component_library = IHMComponentLibrary()
        left_layout.addWidget(self.ihm_component_library, 2)
        
        ihm_layout.addWidget(left_panel)
        
        # Painel central - Canvas de design
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(5, 5, 5, 5)
        
        # Título do canvas
        canvas_title = QLabel("📱 Design da Tela IHM (128x64)")
        canvas_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2d5aa0;
                padding: 8px;
                background-color: #f0f8ff;
                border: 1px solid #b8d4f0;
                border-radius: 4px;
                margin-bottom: 5px;
            }
        """)
        center_layout.addWidget(canvas_title)
        
        # Canvas IHM
        self.ihm_canvas = IHMScreenCanvas()
        center_layout.addWidget(self.ihm_canvas, 1)
        
        # Informações da tela atual
        self.screen_info_label = QLabel("Tela: Nenhuma selecionada")
        self.screen_info_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 3px;
                font-size: 11px;
            }
        """)
        center_layout.addWidget(self.screen_info_label)
        
        ihm_layout.addWidget(center_panel, 1)
        
        # Painel direito - Propriedades
        self.ihm_properties = IHMPropertiesPanel()
        self.ihm_properties.setFixedWidth(250)
        ihm_layout.addWidget(self.ihm_properties)
        
        # Adicionar aba IHM ao tab widget principal
        self.tabs.addTab(ihm_widget, "🖥️ IHM")
        
    def connect_ihm_signals(self):
        """Conecta sinais da interface IHM"""
        # Quando tela é selecionada no gerenciador
        self.screen_manager.screen_selected.connect(self.on_ihm_screen_selected)
        
        # Quando componente é selecionado no canvas
        self.ihm_canvas.component_selected.connect(self.ihm_properties.set_component)
        
        # Atualizar info da tela
        self.screen_manager.screen_selected.connect(self.update_screen_info)
        
    def on_ihm_screen_selected(self, screen):
        """Quando uma tela IHM é selecionada"""
        if screen:
            # Carregar componentes da tela no canvas
            screen_data = []
            for component in screen.components:
                if hasattr(component, 'get_display_data'):
                    screen_data.append(component.get_display_data())
                else:
                    # Converter componente simples para formato esperado
                    screen_data.append({
                        'type': getattr(component, 'type', 'text'),
                        'name': getattr(component, 'name', 'Component'),
                        'x': getattr(component, 'x', 0),
                        'y': getattr(component, 'y', 0),
                        'width': getattr(component, 'width', 16),
                        'height': getattr(component, 'height', 8),
                        'properties': getattr(component, 'properties', {})
                    })
            
            self.ihm_canvas.load_screen_data(screen_data)
            print(f"Tela '{screen.name}' carregada no canvas")
        else:
            self.ihm_canvas.clear_screen()
            
    def update_screen_info(self, screen):
        """Atualiza informações da tela atual"""
        if screen:
            component_count = len(screen.components) if hasattr(screen, 'components') else 0
            info_text = f"Tela: {screen.name} (ID: {screen.id}, {component_count} componentes)"
            self.screen_info_label.setText(info_text)
        else:
            self.screen_info_label.setText("Tela: Nenhuma selecionada")
        
        return self.ladder_canvas
        
    def create_log_area(self):
        """Cria área de logs e saída"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(frame)
        
        # Título
        title = QLabel("📋 Console / Logs")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(title)
        
        # Área de texto para logs
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setPlainText("🚀 Sistema LADDER iniciado\n"
                                  "📡 Aguardando conexão com Raspberry Pi Pico...\n"
                                  "ℹ️  Use 'Configurações > Conexão Pico' para configurar")
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #555;
            }
        """)
        layout.addWidget(self.log_text)
        
        return frame
        
    def create_right_panel(self):
        """Cria painel direito com propriedades"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setMinimumWidth(180)
        frame.setMaximumWidth(250)
        
        layout = QVBoxLayout(frame)
        
        # Título
        title = QLabel("⚙️ Propriedades")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Placeholder para propriedades
        properties_label = QLabel("🔧 Propriedades do elemento selecionado:\n\n"
                                 "• Nome/Tag\n"
                                 "• Tipo\n"
                                 "• Endereço\n"
                                 "• Comentário\n"
                                 "• Configurações específicas\n\n"
                                 "📝 Selecione um elemento no canvas")
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
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Criar novo projeto LADDER')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        # Abrir projeto
        open_action = QAction('📂 &Abrir...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Abrir projeto LADDER existente')
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Salvar
        save_action = QAction('💾 &Salvar', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Salvar projeto atual')
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        # Salvar como
        save_as_action = QAction('💾 Salvar &Como...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.setStatusTip('Salvar projeto com novo nome')
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exportar
        export_menu = file_menu.addMenu('📤 Exportar')
        
        export_python_action = QAction('🐍 Para Python (.py)', self)
        export_python_action.setStatusTip('Exportar código LADDER para Python')
        export_python_action.triggered.connect(self.export_to_python)
        export_menu.addAction(export_python_action)
        
        export_image_action = QAction('🖼️ Como Imagem (.png)', self)
        export_image_action.setStatusTip('Exportar diagrama como imagem')
        export_image_action.triggered.connect(self.export_to_image)
        export_menu.addAction(export_image_action)
        
        file_menu.addSeparator()
        
        # Sair
        exit_action = QAction('🚪 &Sair', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Sair da aplicação')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Editar
        edit_menu = menubar.addMenu('✏️ &Editar')
        
        undo_action = QAction('↶ &Desfazer', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('↷ &Refazer', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        copy_action = QAction('📋 &Copiar', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('📌 Co&lar', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # Menu Pico
        pico_menu = menubar.addMenu('🥧 &Pico')
        
        upload_action = QAction('📤 &Upload para Pico', self)
        upload_action.setShortcut('F5')
        upload_action.setStatusTip('Compilar e enviar código para Raspberry Pi Pico')
        upload_action.triggered.connect(self.upload_to_pico)
        pico_menu.addAction(upload_action)
        
        run_action = QAction('▶️ &Executar no Pico', self)
        run_action.setShortcut('F6')
        run_action.setStatusTip('Executar código no Pico')
        run_action.triggered.connect(self.run_on_pico)
        pico_menu.addAction(run_action)
        
        stop_action = QAction('⏹️ &Parar Execução', self)
        stop_action.setShortcut('F7')
        stop_action.setStatusTip('Parar execução no Pico')
        stop_action.triggered.connect(self.stop_pico)
        pico_menu.addAction(stop_action)
        
        pico_menu.addSeparator()
        
        reset_action = QAction('🔄 &Reset Pico', self)
        reset_action.setStatusTip('Resetar Raspberry Pi Pico')
        reset_action.triggered.connect(self.reset_pico)
        pico_menu.addAction(reset_action)
        
        # Menu Configurações
        config_menu = menubar.addMenu('⚙️ &Configurações')
        
        # Conexão Pico - FUNCIONAL
        pico_config_action = QAction('🔌 &Conexão Pico...', self)
        pico_config_action.setStatusTip('Configurar conexão com Raspberry Pi Pico')
        pico_config_action.triggered.connect(self.open_pico_config)
        config_menu.addAction(pico_config_action)
        
        config_menu.addSeparator()
        
        preferences_action = QAction('🛠️ &Preferências...', self)
        preferences_action.setStatusTip('Configurações gerais da aplicação')
        preferences_action.triggered.connect(self.open_preferences)
        config_menu.addAction(preferences_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu('❓ &Ajuda')
        
        manual_action = QAction('📖 &Manual do Usuário', self)
        manual_action.triggered.connect(self.show_manual)
        help_menu.addAction(manual_action)
        
        about_action = QAction('ℹ️ &Sobre...', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Ações principais
        toolbar.addAction('🆕', self.new_project).setToolTip('Novo projeto')
        toolbar.addAction('📂', self.open_project).setToolTip('Abrir projeto')
        toolbar.addAction('💾', self.save_project).setToolTip('Salvar projeto')
        
        toolbar.addSeparator()
        
        toolbar.addAction('↶', self.undo).setToolTip('Desfazer')
        toolbar.addAction('↷', self.redo).setToolTip('Refazer')
        
        toolbar.addSeparator()
        
        toolbar.addAction('📤', self.upload_to_pico).setToolTip('Upload para Pico')
        toolbar.addAction('▶️', self.run_on_pico).setToolTip('Executar no Pico')
        toolbar.addAction('⏹️', self.stop_pico).setToolTip('Parar execução')
        
        toolbar.addSeparator()
        
        toolbar.addAction('🔌', self.open_pico_config).setToolTip('Configurar conexão Pico')
        
    def create_status_bar(self):
        """Cria a barra de status"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status da conexão
        self.connection_status = QLabel("🔴 Desconectado")
        self.status_bar.addPermanentWidget(self.connection_status)
        
        # Status geral
        self.status_bar.showMessage("Pronto - Interface LADDER para Raspberry Pi Pico")
        
    def apply_style(self):
        """Aplica estilos à janela"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #ddd;
                padding: 2px;
            }
            QMenuBar::item {
                padding: 4px 8px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QToolBar {
                background-color: #ffffff;
                border: 1px solid #ddd;
                spacing: 3px;
                padding: 2px;
            }
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #ddd;
            }
        """)
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.append(f"[{self.get_timestamp()}] {message}")
        
    def get_timestamp(self):
        """Retorna timestamp atual"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def update_connection_status(self, connected, port=None):
        """Atualiza status da conexão"""
        if connected:
            self.connection_status.setText(f"🟢 Conectado: {port}")
            self.log_message(f"✅ Conectado ao Pico em {port}")
        else:
            self.connection_status.setText("🔴 Desconectado")
            self.log_message("❌ Desconectado do Pico")
    
    # ================== SLOTS DOS MENUS ==================
    
    def new_project(self):
        """Criar novo projeto"""
        self.log_message("🆕 Novo projeto criado")
        
    def open_project(self):
        """Abrir projeto"""
        self.log_message("📂 Abrir projeto - Em desenvolvimento")
        
    def save_project(self):
        """Salvar projeto"""
        self.log_message("💾 Salvar projeto - Em desenvolvimento")
        
    def save_project_as(self):
        """Salvar projeto como"""
        self.log_message("💾 Salvar como - Em desenvolvimento")
        
    def export_to_python(self):
        """Exportar para Python"""
        self.log_message("🐍 Exportar para Python - Em desenvolvimento")
        
    def export_to_image(self):
        """Exportar como imagem"""
        self.log_message("🖼️ Exportar como imagem - Em desenvolvimento")
        
    def undo(self):
        """Desfazer"""
        self.log_message("↶ Desfazer - Em desenvolvimento")
        
    def redo(self):
        """Refazer"""
        self.log_message("↷ Refazer - Em desenvolvimento")
        
    def copy(self):
        """Copiar"""
        self.log_message("📋 Copiar - Em desenvolvimento")
        
    def paste(self):
        """Colar"""
        self.log_message("📌 Colar - Em desenvolvimento")
        
    def upload_to_pico(self):
        """Upload para Pico"""
        self.log_message("📤 Upload para Pico - Em desenvolvimento")
        
    def run_on_pico(self):
        """Executar no Pico"""
        self.log_message("▶️ Executar no Pico - Em desenvolvimento")
        
    def stop_pico(self):
        """Parar execução no Pico"""
        self.log_message("⏹️ Parar execução - Em desenvolvimento")
        
    def reset_pico(self):
        """Reset Pico"""
        self.log_message("🔄 Reset Pico - Em desenvolvimento")
        
    def open_pico_config(self):
        """Abrir configurações do Pico - FUNCIONAL"""
        if self.config_dialog is None:
            self.config_dialog = ConfigDialog(self)
            # Conectar sinais
            self.config_dialog.connection_changed.connect(self.update_connection_status)
            self.config_dialog.log_message.connect(self.log_message)
            
        self.config_dialog.show()
        self.config_dialog.raise_()
        self.config_dialog.activateWindow()
        
    def open_preferences(self):
        """Abrir preferências"""
        self.log_message("🛠️ Preferências - Em desenvolvimento")
        
    def show_manual(self):
        """Mostrar manual"""
        self.log_message("📖 Manual do usuário - Em desenvolvimento")
        
    def show_about(self):
        """Mostrar sobre"""
        QMessageBox.about(self, "Sobre CLP-IHM-PICO",
                         """<h2>CLP-IHM-PICO</h2>
                         <p>Interface LADDER para Raspberry Pi Pico</p>
                         <p><b>Versão:</b> 1.0.0 Beta</p>
                         <p><b>Desenvolvido por:</b> Renato</p>
                         <p><b>Data:</b> Outubro 2025</p>
                         <hr>
                         <p>Sistema de programação visual tipo LADDER para controle industrial usando Raspberry Pi Pico.</p>
                         """)
    
    # ================== EVENTOS DOS COMPONENTES ==================
    
    def on_component_selected(self, component):
        """Chamado quando um componente é selecionado no canvas"""
        if component:
            self.log_message(f"Selecionado: {component.name} ({component.component_type})")
            # TODO: Atualizar painel de propriedades
        else:
            self.log_message("Nenhum componente selecionado")
            
    def on_component_added(self, component_type, name):
        """Chamado quando um componente é adicionado ao canvas"""
        self.log_message(f"Componente adicionado: {name} ({component_type})")
        
        # Atualizar status
        if hasattr(self, 'ladder_canvas'):
            count = len(self.ladder_canvas.components)
            self.status_bar.showMessage(f"Canvas com {count} componente(s) - {component_type} adicionado")
        

def main():
    """Função principal"""
    app = QApplication(sys.argv)
    app.setApplicationName("CLP-IHM-PICO")
    app.setOrganizationName("RenatoDevs")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
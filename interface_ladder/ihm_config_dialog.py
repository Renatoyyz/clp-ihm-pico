"""
Janela de Configuração IHM
Popup para configurar telas do Display ST7920 quando bloco IHM é clicado
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QPushButton, QSplitter, QWidget, QApplication, QGroupBox, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class IHMConfigDialog(QDialog):
    """Janela de configuração do Display IHM"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🖥️ Configuração Display IHM - ST7920 (128x64)")
        self.setGeometry(200, 200, 1200, 800)
        self.setModal(True)  # Janela modal
        
        # Inicializar componentes IHM
        self.init_ihm_components()
        
        # Inicializar interface
        self.init_ui()
        
    def init_ihm_components(self):
        """Inicializa componentes IHM importados dinamicamente"""
        try:
            # Importar componentes IHM quando necessário
            from ihm_components import IHMComponentLibrary
            from ihm_canvas import IHMScreenCanvas, IHMPropertiesPanel
            from ihm_screen_manager import IHMScreenManager
            
            self.IHMComponentLibrary = IHMComponentLibrary
            self.IHMScreenCanvas = IHMScreenCanvas
            self.IHMPropertiesPanel = IHMPropertiesPanel 
            self.IHMScreenManager = IHMScreenManager
            
            self.ihm_available = True
            print("✅ Componentes IHM carregados com sucesso")
            
        except ImportError as e:
            print(f"⚠️ Erro ao carregar componentes IHM: {e}")
            self.ihm_available = False
        
    def init_ui(self):
        """Inicializa interface da janela"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título principal
        title = QLabel("🖥️ Configuração do Display IHM ST7920")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #2d5aa0;
                background-color: #f0f8ff;
                padding: 15px;
                border: 2px solid #b8d4f0;
                border-radius: 8px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        if self.ihm_available:
            # Criar interface completa IHM
            self.create_ihm_interface(layout)
        else:
            # Mostrar mensagem de erro
            self.create_error_interface(layout)
            
        # Botões de controle
        self.create_control_buttons(layout)
        
    def create_ihm_interface(self, layout):
        """Cria interface completa do IHM"""
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Painel esquerdo - Configuração da tela única
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Configuração da tela única
        screen_config_group = QGroupBox("🖥️ Configuração da Tela")
        screen_config_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #17a2b8;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 8px;
                background-color: #17a2b8;
                color: white;
                border-radius: 4px;
                margin-left: 5px;
            }
        """)
        screen_config_layout = QVBoxLayout(screen_config_group)
        
        # Nome da tela
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nome:"))
        self.screen_name_field = QLineEdit("Tela Display")
        self.screen_name_field.setPlaceholderText("Digite o nome da tela...")
        name_layout.addWidget(self.screen_name_field)
        screen_config_layout.addLayout(name_layout)
        
        # Informações da tela
        info_text = QLabel("• Uma tela por bloco Display\n• 128×64 pixels (ST7920)\n• Configure os componentes abaixo")
        info_text.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 11px;
                padding: 8px;
                background-color: #f8f9fa;
                border-radius: 4px;
                margin: 5px 0px;
            }
        """)
        screen_config_layout.addWidget(info_text)
        
        left_layout.addWidget(screen_config_group)
        
        # Biblioteca de componentes IHM
        self.ihm_library = self.IHMComponentLibrary()
        left_layout.addWidget(self.ihm_library, 1)
        
        main_splitter.addWidget(left_panel)
        
        # Painel central - Canvas
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(10, 5, 10, 5)
        
        # Título do canvas
        canvas_title = QLabel("📱 Design da Tela (128x64 pixels)")
        canvas_title.setFont(QFont("Arial", 12, QFont.Bold))
        canvas_title.setAlignment(Qt.AlignCenter)
        canvas_title.setStyleSheet("""
            QLabel {
                color: #228b22;
                background-color: #f0fff0;
                padding: 8px;
                border: 1px solid #90ee90;
                border-radius: 5px;
                margin-bottom: 8px;
            }
        """)
        center_layout.addWidget(canvas_title)
        
        # Canvas de design
        self.ihm_canvas = self.IHMScreenCanvas()
        center_layout.addWidget(self.ihm_canvas)
        
        # Info da tela única
        self.screen_info = QLabel("Tela: Tela Display - 0 componentes")
        self.screen_info.setStyleSheet("""
            QLabel {
                padding: 5px;
                background-color: #e8f4fd;
                border: 1px solid #17a2b8;
                border-radius: 3px;
                font-size: 11px;
                color: #17a2b8;
                font-weight: bold;
            }
        """)
        center_layout.addWidget(self.screen_info)
        
        main_splitter.addWidget(center_panel)
        
        # Painel direito - Propriedades
        self.properties_panel = self.IHMPropertiesPanel()
        self.properties_panel.setFixedWidth(250)
        main_splitter.addWidget(self.properties_panel)
        
        # Configurar proporções do splitter após adicionar todos os widgets
        main_splitter.setSizes([300, 600, 250])
        
        layout.addWidget(main_splitter, 1)
        
        # Conectar sinais
        self.connect_ihm_signals()
        
    def create_error_interface(self, layout):
        """Cria interface de erro quando IHM não disponível"""
        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)
        
        # Mensagem de erro
        error_msg = QLabel("""
        ⚠️ Componentes IHM não disponíveis
        
        Os módulos necessários para a interface IHM não foram encontrados:
        • ihm_components.py
        • ihm_canvas.py  
        • ihm_screen_manager.py
        
        Verifique se os arquivos estão presentes no diretório.
        """)
        error_msg.setFont(QFont("Arial", 12))
        error_msg.setAlignment(Qt.AlignCenter)
        error_msg.setStyleSheet("""
            QLabel {
                color: #721c24;
                background-color: #f8d7da;
                padding: 20px;
                border: 2px solid #f5c6cb;
                border-radius: 8px;
                margin: 20px;
            }
        """)
        error_layout.addWidget(error_msg)
        
        layout.addWidget(error_widget, 1)
        
    def create_control_buttons(self, layout):
        """Cria botões de controle da janela"""
        buttons_layout = QHBoxLayout()
        
        if self.ihm_available:
            # Botão Aplicar
            apply_btn = QPushButton("✅ Aplicar")
            apply_btn.clicked.connect(self.apply_configuration)
            apply_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            buttons_layout.addWidget(apply_btn)
            
        # Botão Fechar  
        close_btn = QPushButton("❌ Fechar")
        close_btn.clicked.connect(self.reject)  # Usar reject ao invés de accept
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)
        buttons_layout.addWidget(close_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
    def connect_ihm_signals(self):
        """Conecta sinais da interface IHM"""
        if not self.ihm_available:
            return
            
        # Conectar seleção de componente
        self.ihm_canvas.component_selected.connect(self.properties_panel.set_component)
        
        # Conectar mudanças de componentes para atualizar informações
        self.ihm_canvas.components_changed.connect(self.update_screen_info)
        
        # Conectar biblioteca de componentes para adicionar ao canvas
        self.ihm_library.add_component_requested.connect(self.add_component_to_canvas)
        
        # Conectar mudanças no nome da tela
        self.screen_name_field.textChanged.connect(self.update_screen_info)
                
    def add_component_to_canvas(self, comp_type, comp_name):
        """Adiciona componente ao canvas IHM"""
        if self.ihm_available and hasattr(self, 'ihm_canvas'):
            # Posicionar no centro da tela (ou próximo)
            center_x = 64 - 16  # Centro menos metade do componente
            center_y = 32 - 8   # Centro menos metade do componente
            
            # Adicionar pequeno offset para não sobrepor
            offset = len(self.ihm_canvas.screen_components) * 10
            x = max(5, center_x + offset)
            y = max(5, center_y + (offset // 2))
            
            # Garantir que não saia da tela
            x = min(x, 128 - 16)
            y = min(y, 64 - 8)
            
            # Adicionar componente ao canvas
            self.ihm_canvas.add_component(comp_type, x, y)
            print(f"✅ Componente '{comp_name}' adicionado ao canvas em ({x}, {y})")
            

        
    def update_screen_info(self):
        """Atualiza informações da tela única"""
        screen_name = self.screen_name_field.text() or "Tela Display"
        component_count = len(getattr(self.ihm_canvas, 'screen_components', []))
        self.screen_info.setText(f"Tela: {screen_name} - {component_count} componente(s)")
        
    def get_screen_data(self):
        """Obtém dados da tela única configurada"""
        screen_name = self.screen_name_field.text() or "Tela Display"
        components_data = []
        
        # Coletar dados dos componentes no canvas
        if hasattr(self.ihm_canvas, 'screen_components'):
            for comp_data in self.ihm_canvas.screen_components:
                component = comp_data['component']
                components_data.append({
                    'type': getattr(component, 'type', 'text'),
                    'name': getattr(component, 'name', 'Component'),
                    'x': getattr(component, 'x', 0),
                    'y': getattr(component, 'y', 0),
                    'width': getattr(component, 'width', 16),
                    'height': getattr(component, 'height', 8),
                    'properties': getattr(component, 'properties', {})
                })
        
        return {
            'name': screen_name,
            'components': components_data,
            'properties': {
                'background_color': 'light_green',
                'timeout': 0,
                'show_header': True
            }
        }
            
    def load_saved_data(self, config_data):
        """Carrega dados salvos anteriormente"""
        if not config_data or not self.ihm_available:
            return
            
        # Carregar nome da tela
        if 'screen_name' in config_data:
            self.screen_name_field.setText(config_data['screen_name'])
        
        # Carregar componentes no canvas
        if 'components' in config_data and config_data['components']:
            components_data = config_data['components']
            self.ihm_canvas.load_screen_data(components_data)
            print(f"📁 Carregados {len(components_data)} componente(s) salvos")
        
        # Atualizar informações da tela
        self.update_screen_info()

    def apply_configuration(self):
        """Aplica configurações da tela única"""
        if self.ihm_available:
            screen_data = self.get_screen_data()
            screen_name = screen_data['name']
            component_count = len(screen_data['components'])
            
            print(f"✅ Configuração da tela '{screen_name}' aplicada")
            print(f"📊 {component_count} componente(s) configurados")
            
            # Fechar dialog com sucesso
            self.accept()
            

            
    def closeEvent(self, event):
        """Evento de fechamento da janela"""
        print("🖥️ Janela de configuração IHM fechada")
        event.accept()

# Função auxiliar para abrir a janela
def show_ihm_dialog(parent=None):
    """Abre janela de configuração IHM"""
    dialog = IHMConfigDialog(parent)
    return dialog.exec_()

# Teste da janela
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = IHMConfigDialog()
    dialog.show()
    
    sys.exit(app.exec_())
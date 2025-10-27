"""
Gerenciador de Telas IHM
Sistema para gerenciar múltiplas telas do display ST7920

Permite criar, editar e navegar entre diferentes telas da interface
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QPushButton, QListWidget, QListWidgetItem,
                           QTabWidget, QInputDialog, QMessageBox, QSplitter,
                           QFrame, QGroupBox, QComboBox, QSpinBox,
                           QTextEdit, QCheckBox, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
import json
import copy
import os

class IHMScreen:
    """Representa uma tela IHM"""
    
    def __init__(self, name="Nova Tela", screen_id=1):
        self.name = name
        self.id = screen_id
        self.components = []  # Lista de componentes na tela
        self.properties = {
            'background_color': 'light_green',
            'timeout': 0,  # Timeout em segundos (0 = sem timeout)
            'next_screen': 0,  # Tela para navegar após timeout
            'show_header': True,
            'header_text': '',
            'show_footer': False,
            'footer_text': ''
        }
        
    def add_component(self, component):
        """Adiciona componente à tela"""
        self.components.append(component)
        
    def remove_component(self, component):
        """Remove componente da tela"""
        if component in self.components:
            self.components.remove(component)
            
    def get_screen_data(self):
        """Retorna dados da tela para serialização"""
        return {
            'name': self.name,
            'id': self.id,
            'components': [comp.get_display_data() for comp in self.components],
            'properties': self.properties
        }
        
    def load_screen_data(self, data):
        """Carrega dados da tela"""
        self.name = data.get('name', 'Tela')
        self.id = data.get('id', 1)
        self.properties = data.get('properties', {})
        # Componentes serão carregados separadamente pelo canvas

class IHMScreenManager(QWidget):
    """Gerenciador de telas IHM"""
    
    screen_changed = pyqtSignal(object)  # Emite quando tela muda
    screen_selected = pyqtSignal(object)  # Emite quando tela é selecionada
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Lista de telas
        self.screens = []
        self.current_screen = None
        self.current_screen_index = 0
        
        # Criar tela inicial
        self.create_default_screen()
        
        # Inicializar interface
        self.init_ui()
        
    def init_ui(self):
        """Inicializa interface do gerenciador"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Título
        title = QLabel("📱 Gerenciador de Telas")
        title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2d5aa0;
                padding: 8px;
                background-color: #f0f8ff;
                border: 1px solid #b8d4f0;
                border-radius: 4px;
            }
        """)
        layout.addWidget(title)
        
        # Botões de controle
        self.create_control_buttons(layout)
        
        # Lista de telas
        self.create_screen_list(layout)
        
        # Propriedades da tela atual
        self.create_screen_properties(layout)
        
    def create_control_buttons(self, layout):
        """Cria botões de controle"""
        buttons_layout = QHBoxLayout()
        
        # Botão Nova Tela
        btn_new = QPushButton("➕ Nova Tela")
        btn_new.clicked.connect(self.add_new_screen)
        btn_new.setToolTip("Criar nova tela")
        buttons_layout.addWidget(btn_new)
        
        # Botão Duplicar
        btn_duplicate = QPushButton("📋 Duplicar")
        btn_duplicate.clicked.connect(self.duplicate_screen)
        btn_duplicate.setToolTip("Duplicar tela atual")
        buttons_layout.addWidget(btn_duplicate)
        
        # Botão Excluir
        btn_delete = QPushButton("🗑️ Excluir")
        btn_delete.clicked.connect(self.delete_screen)
        btn_delete.setToolTip("Excluir tela atual")
        buttons_layout.addWidget(btn_delete)
        
        layout.addLayout(buttons_layout)
        
    def create_screen_list(self, layout):
        """Cria lista de telas"""
        # Grupo da lista
        group = QGroupBox("📋 Lista de Telas")
        group_layout = QVBoxLayout(group)
        
        # Lista
        self.screen_list = QListWidget()
        self.screen_list.currentRowChanged.connect(self.on_screen_selected)
        group_layout.addWidget(self.screen_list)
        
        # Botões de navegação
        nav_layout = QHBoxLayout()
        
        btn_up = QPushButton("⬆️")
        btn_up.clicked.connect(self.move_screen_up)
        btn_up.setFixedSize(30, 30)
        btn_up.setToolTip("Mover para cima")
        nav_layout.addWidget(btn_up)
        
        btn_down = QPushButton("⬇️")
        btn_down.clicked.connect(self.move_screen_down)
        btn_down.setFixedSize(30, 30)
        btn_down.setToolTip("Mover para baixo")
        nav_layout.addWidget(btn_down)
        
        nav_layout.addStretch()
        
        group_layout.addLayout(nav_layout)
        layout.addWidget(group)
        
    def create_screen_properties(self, layout):
        """Cria painel de propriedades da tela"""
        # Grupo de propriedades
        group = QGroupBox("⚙️ Propriedades da Tela")
        group_layout = QFormLayout(group)
        
        # Nome da tela
        self.name_edit = QInputDialog()
        self.name_label = QLabel("Clique para editar nome")
        self.name_label.mousePressEvent = self.edit_screen_name
        self.name_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                padding: 4px;
                background-color: white;
            }
            QLabel:hover {
                background-color: #f0f0f0;
            }
        """)
        group_layout.addRow("Nome:", self.name_label)
        
        # Timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(0, 300)  # 0 a 5 minutos
        self.timeout_spin.setSuffix(" seg")
        self.timeout_spin.setSpecialValueText("Sem timeout")
        self.timeout_spin.valueChanged.connect(self.update_screen_properties)
        group_layout.addRow("Timeout:", self.timeout_spin)
        
        # Tela seguinte
        self.next_screen_combo = QComboBox()
        self.next_screen_combo.currentTextChanged.connect(self.update_screen_properties)
        group_layout.addRow("Próxima tela:", self.next_screen_combo)
        
        # Mostrar cabeçalho
        self.show_header_check = QCheckBox()
        self.show_header_check.toggled.connect(self.update_screen_properties)
        group_layout.addRow("Mostrar cabeçalho:", self.show_header_check)
        
        # Texto do cabeçalho
        self.header_text_edit = QTextEdit()
        self.header_text_edit.setMaximumHeight(50)
        self.header_text_edit.textChanged.connect(self.update_screen_properties)
        group_layout.addRow("Texto cabeçalho:", self.header_text_edit)
        
        layout.addWidget(group)
        
    def create_default_screen(self):
        """Cria tela padrão inicial"""
        screen = IHMScreen("Tela Principal", 1)
        screen.properties['header_text'] = "Sistema CLP"
        self.screens.append(screen)
        self.current_screen = screen
        
    def add_new_screen(self):
        """Adiciona nova tela"""
        # Pedir nome da tela
        name, ok = QInputDialog.getText(self, "Nova Tela", "Nome da tela:")
        if ok and name:
            # Criar nova tela
            screen_id = len(self.screens) + 1
            screen = IHMScreen(name, screen_id)
            self.screens.append(screen)
            
            # Atualizar interface
            self.update_screen_list()
            self.screen_list.setCurrentRow(len(self.screens) - 1)
            
            print(f"Nova tela criada: {name}")
            
    def duplicate_screen(self):
        """Duplica tela atual"""
        if not self.current_screen:
            return
            
        # Pedir nome da nova tela
        name, ok = QInputDialog.getText(self, "Duplicar Tela", 
                                      f"Nome da cópia:", 
                                      text=f"{self.current_screen.name} - Cópia")
        if ok and name:
            # Criar cópia
            screen_id = len(self.screens) + 1
            new_screen = IHMScreen(name, screen_id)
            new_screen.properties = copy.deepcopy(self.current_screen.properties)
            new_screen.components = copy.deepcopy(self.current_screen.components)
            
            self.screens.append(new_screen)
            
            # Atualizar interface
            self.update_screen_list()
            self.screen_list.setCurrentRow(len(self.screens) - 1)
            
            print(f"Tela duplicada: {name}")
            
    def delete_screen(self):
        """Exclui tela atual"""
        if len(self.screens) <= 1:
            QMessageBox.warning(self, "Aviso", "Não é possível excluir a última tela!")
            return
            
        if not self.current_screen:
            return
            
        # Confirmar exclusão
        reply = QMessageBox.question(self, "Confirmar Exclusão",
                                   f"Deseja excluir a tela '{self.current_screen.name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Remover tela
            self.screens.remove(self.current_screen)
            
            # Selecionar tela anterior
            if self.current_screen_index >= len(self.screens):
                self.current_screen_index = len(self.screens) - 1
                
            self.current_screen = self.screens[self.current_screen_index]
            
            # Atualizar interface
            self.update_screen_list()
            self.screen_list.setCurrentRow(self.current_screen_index)
            
            print(f"Tela excluída")
            
    def move_screen_up(self):
        """Move tela para cima na lista"""
        current_row = self.screen_list.currentRow()
        if current_row > 0:
            # Trocar posições
            self.screens[current_row], self.screens[current_row - 1] = \
                self.screens[current_row - 1], self.screens[current_row]
            
            # Atualizar interface
            self.update_screen_list()
            self.screen_list.setCurrentRow(current_row - 1)
            
    def move_screen_down(self):
        """Move tela para baixo na lista"""
        current_row = self.screen_list.currentRow()
        if current_row < len(self.screens) - 1:
            # Trocar posições
            self.screens[current_row], self.screens[current_row + 1] = \
                self.screens[current_row + 1], self.screens[current_row]
            
            # Atualizar interface
            self.update_screen_list()
            self.screen_list.setCurrentRow(current_row + 1)
            
    def on_screen_selected(self, row):
        """Quando uma tela é selecionada"""
        if 0 <= row < len(self.screens):
            self.current_screen_index = row
            self.current_screen = self.screens[row]
            self.update_properties_panel()
            self.screen_selected.emit(self.current_screen)
            
    def edit_screen_name(self, event):
        """Edita nome da tela"""
        if not self.current_screen:
            return
            
        name, ok = QInputDialog.getText(self, "Editar Nome", 
                                      "Nome da tela:", 
                                      text=self.current_screen.name)
        if ok and name:
            self.current_screen.name = name
            self.update_screen_list()
            self.update_properties_panel()
            
    def update_screen_properties(self):
        """Atualiza propriedades da tela atual"""
        if not self.current_screen:
            return
            
        # Atualizar propriedades
        props = self.current_screen.properties
        props['timeout'] = self.timeout_spin.value()
        props['show_header'] = self.show_header_check.isChecked()
        props['header_text'] = self.header_text_edit.toPlainText()
        
        # Próxima tela
        next_text = self.next_screen_combo.currentText()
        if next_text and next_text != "Nenhuma":
            try:
                props['next_screen'] = int(next_text.split(" ")[1])
            except:
                props['next_screen'] = 0
        else:
            props['next_screen'] = 0
            
    def update_properties_panel(self):
        """Atualiza painel de propriedades"""
        if not self.current_screen:
            return
            
        screen = self.current_screen
        props = screen.properties
        
        # Nome
        self.name_label.setText(screen.name)
        
        # Timeout
        self.timeout_spin.setValue(props.get('timeout', 0))
        
        # Próxima tela
        self.next_screen_combo.clear()
        self.next_screen_combo.addItem("Nenhuma")
        for i, scr in enumerate(self.screens):
            if scr != screen:
                self.next_screen_combo.addItem(f"Tela {scr.id}")
                
        # Cabeçalho
        self.show_header_check.setChecked(props.get('show_header', True))
        self.header_text_edit.setPlainText(props.get('header_text', ''))
        
    def update_screen_list(self):
        """Atualiza lista de telas"""
        self.screen_list.clear()
        
        for i, screen in enumerate(self.screens):
            item_text = f"Tela {screen.id}: {screen.name}"
            if len(screen.components) > 0:
                item_text += f" ({len(screen.components)} componentes)"
                
            item = QListWidgetItem(item_text)
            
            # Ícone baseado no tipo de tela
            if screen.properties.get('show_header', True):
                item.setIcon(self.create_screen_icon("📱"))
            else:
                item.setIcon(self.create_screen_icon("📄"))
                
            self.screen_list.addItem(item)
            
        # Atualizar combo de próxima tela
        self.update_properties_panel()
        
    def create_screen_icon(self, emoji):
        """Cria ícone para tela"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(0, 12, emoji)
        painter.end()
        
        return QIcon(pixmap)
        
    def get_current_screen(self):
        """Retorna tela atual"""
        return self.current_screen
        
    def get_all_screens(self):
        """Retorna todas as telas"""
        return self.screens
        
    def save_screens_data(self):
        """Salva dados de todas as telas"""
        return [screen.get_screen_data() for screen in self.screens]
        
    def load_screens_data(self, screens_data):
        """Carrega dados das telas"""
        self.screens.clear()
        
        for screen_data in screens_data:
            screen = IHMScreen()
            screen.load_screen_data(screen_data)
            self.screens.append(screen)
            
        if self.screens:
            self.current_screen = self.screens[0]
            self.current_screen_index = 0
        else:
            self.create_default_screen()
            
        self.update_screen_list()
        
    def save_configuration(self, filename="ihm_config.json"):
        """Salva configuração completa das telas em arquivo JSON"""
        try:
            # Preparar dados para salvamento
            config_data = {
                'version': '1.0',
                'screens': [],
                'current_screen_index': self.current_screen_index,
                'total_screens': len(self.screens)
            }
            
            # Salvar dados de cada tela
            for screen in self.screens:
                screen_data = {
                    'name': screen.name,
                    'id': screen.id,
                    'properties': screen.properties,
                    'components': []
                }
                
                # Salvar componentes da tela
                for component in screen.components:
                    comp_data = {
                        'type': getattr(component, 'type', 'unknown'),
                        'name': getattr(component, 'name', 'Component'),
                        'x': getattr(component, 'x', 0),
                        'y': getattr(component, 'y', 0),
                        'width': getattr(component, 'width', 16),
                        'height': getattr(component, 'height', 8),
                        'properties': getattr(component, 'properties', {})
                    }
                    screen_data['components'].append(comp_data)
                
                config_data['screens'].append(screen_data)
            
            # Salvar em arquivo
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Configuração IHM salva em '{filename}'")
            print(f"📊 {len(self.screens)} telas salvas com {sum(len(s.components) for s in self.screens)} componentes")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
            return False
    
    def load_configuration(self, filename="ihm_config.json"):
        """Carrega configuração das telas de arquivo JSON"""
        try:
            # Verificar se arquivo existe
            if not os.path.exists(filename):
                print(f"⚠️ Arquivo '{filename}' não encontrado, usando configuração padrão")
                return False
            
            # Carregar dados
            with open(filename, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Limpar telas atuais
            self.screens.clear()
            
            # Carregar telas
            for screen_data in config_data.get('screens', []):
                screen = IHMScreen(
                    name=screen_data.get('name', 'Tela'),
                    screen_id=screen_data.get('id', 1)
                )
                screen.properties = screen_data.get('properties', {})
                
                # Carregar componentes
                for comp_data in screen_data.get('components', []):
                    # Criar objeto básico de componente para carregar
                    from ihm_components import IHMComponent
                    component = IHMComponent(
                        name=comp_data.get('name', 'Component'),
                        component_type=comp_data.get('type', 'text'),
                        category='loaded'
                    )
                    component.x = comp_data.get('x', 0)
                    component.y = comp_data.get('y', 0)
                    component.width = comp_data.get('width', 16)
                    component.height = comp_data.get('height', 8)
                    component.properties = comp_data.get('properties', {})
                    screen.components.append(component)
                
                self.screens.append(screen)
            
            # Restaurar índice da tela atual
            self.current_screen_index = config_data.get('current_screen_index', 0)
            if self.current_screen_index >= len(self.screens):
                self.current_screen_index = 0
                
            # Se não há telas, criar uma padrão
            if not self.screens:
                self.create_default_screen()
            else:
                self.current_screen = self.screens[self.current_screen_index] if self.screens else None
            
            # Atualizar interface
            self.update_screen_list()
            if self.current_screen:
                self.screen_selected.emit(self.current_screen)
            
            print(f"📁 Configuração carregada de '{filename}'")
            print(f"📊 {len(self.screens)} telas carregadas com {sum(len(s.components) for s in self.screens)} componentes")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            # Em caso de erro, criar tela padrão
            self.screens.clear()
            self.create_default_screen()
            self.update_screen_list()
            return False

# Widget de teste
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Teste Gerenciador de Telas")
    window.setGeometry(100, 100, 400, 600)
    
    manager = IHMScreenManager()
    window.setCentralWidget(manager)
    
    window.show()
    
    sys.exit(app.exec_())
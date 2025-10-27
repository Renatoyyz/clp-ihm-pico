"""
Biblioteca de Componentes para Interface IHM
Display ST7920 128x64 pixels

Componentes visuais para criação de telas de interface humano-máquina
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QScrollArea, QFrame, QPushButton, QGroupBox,
                           QApplication)
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QDrag, QPainter, QColor, QFont, QPen, QBrush, QPixmap, QPolygon

class IHMComponent:
    """Componente base para elementos de IHM"""
    def __init__(self, name, component_type, category):
        self.name = name
        self.type = component_type
        self.category = category
        self.x = 0
        self.y = 0
        self.width = 20
        self.height = 8
        self.properties = {}
        
    def get_display_data(self):
        """Retorna dados para renderização no display ST7920"""
        return {
            'type': self.type,
            'name': self.name,
            'x': self.x,
            'y': self.y, 
            'width': self.width,
            'height': self.height,
            'properties': self.properties
        }

class IHMComponentWidget(QLabel):
    """Widget visual para componente IHM na biblioteca"""
    
    def __init__(self, component, parent=None):
        super().__init__(parent)
        self.component = component
        self.setFixedSize(120, 60)
        self.setStyleSheet("""
            QLabel {
                border: 1px solid #666;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
                background-color: white;
            }
            QLabel:hover {
                background-color: #e6f3ff;
                border: 2px solid #0078d4;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.update_display()
        
    def update_display(self):
        """Atualiza a visualização do componente"""
        pixmap = QPixmap(116, 56)
        pixmap.fill(QColor(255, 255, 255))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenha preview do componente baseado no tipo
        self.draw_component_preview(painter)
        
        # Adiciona nome do componente
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setFont(QFont("Arial", 8))
        painter.drawText(2, 50, self.component.name)
        
        painter.end()
        self.setPixmap(pixmap)
        
    def draw_component_preview(self, painter):
        """Desenha preview específico do tipo de componente - IHM OP320 Style"""
        comp = self.component
        
        if comp.type == 'static_text':
            # Texto estático
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(10, 20, "Texto ABC")
            painter.setFont(QFont("Arial", 7))
            painter.drawText(10, 35, "Estático")
            
        elif comp.type == 'dynamic_text':
            # Texto dinâmico (variável)
            painter.setPen(QPen(QColor(0, 120, 0), 1))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(10, 20, "123.45")
            painter.setFont(QFont("Arial", 7))
            painter.drawText(10, 35, "Dinâmico")
            
        elif comp.type == 'led_indicator':
            # LED Indicador - Mais estilizado e redondo
            # Círculo externo (borda)
            painter.setPen(QPen(QColor(100, 100, 100), 2))
            painter.setBrush(QBrush(QColor(200, 200, 200)))
            painter.drawEllipse(40, 12, 20, 20)
            
            # LED interno com efeito de profundidade
            color = QColor(0, 255, 0)  # Verde por padrão
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(150), 1))
            painter.drawEllipse(42, 14, 16, 16)
            
            # Brilho no LED (efeito 3D)
            painter.setBrush(QBrush(QColor(255, 255, 255, 180)))
            painter.setPen(QPen(QColor(255, 255, 255, 0)))
            painter.drawEllipse(44, 16, 6, 6)
            
            painter.setFont(QFont("Arial", 7))
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawText(35, 45, "LED")
            
        elif comp.type == 'input_field':
            # Campo de entrada
            painter.setPen(QPen(QColor(0, 120, 215), 2))
            painter.drawRect(10, 15, 80, 15)
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(12, 26, "123.45")
            painter.setFont(QFont("Arial", 7))
            painter.drawText(10, 40, "Entrada")
            
        elif comp.type == 'function_button':
            # Botão de função (F1-F4) - Formato de seta estilizado
            # Fundo do botão
            painter.setBrush(QBrush(QColor(255, 200, 100)))
            painter.setPen(QPen(QColor(200, 150, 50), 2))
            painter.drawRoundedRect(10, 12, 80, 18, 3, 3)
            
            # Desenhar seta apontando para direita
            arrow_points = [
                QPoint(20, 21),   # Ponta esquerda da seta
                QPoint(35, 15),   # Ponta superior da cabeça
                QPoint(30, 18),   # Base superior da cabeça
                QPoint(40, 18),   # Extremidade direita da haste
                QPoint(40, 24),   # Extremidade direita da haste (baixo)
                QPoint(30, 24),   # Base inferior da cabeça
                QPoint(35, 27)    # Ponta inferior da cabeça
            ]
            
            arrow_polygon = QPolygon(arrow_points)
            painter.setBrush(QBrush(QColor(100, 50, 0)))
            painter.setPen(QPen(QColor(80, 40, 0), 1))
            painter.drawPolygon(arrow_polygon)
            
            # Texto do botão
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setFont(QFont("Arial", 8, QFont.Bold))
            painter.drawText(50, 24, "F1")
            painter.setFont(QFont("Arial", 7))
            painter.drawText(25, 40, "Função")
            
        elif comp.type == 'mono_image':
            # Área de imagem monocromática
            painter.setPen(QPen(QColor(100, 100, 100), 1))
            painter.drawRect(10, 10, 80, 30)
            # Desenhar grade para representar pixels
            for i in range(3):
                painter.drawLine(10 + i*20, 10, 10 + i*20, 40)
            for i in range(2):
                painter.drawLine(10, 10 + i*15, 90, 10 + i*15)
            painter.setFont(QFont("Arial", 7))
            painter.drawText(25, 50, "Imagem")
            
        elif comp.type == 'bar_graph':
            # Gráfico de barras
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(10, 10, 80, 30)
            painter.setBrush(QBrush(QColor(0, 120, 215)))
            painter.drawRect(12, 25, 15, 15)
            painter.drawRect(30, 20, 15, 20)
            painter.drawRect(48, 15, 15, 25)
            painter.drawRect(66, 22, 15, 18)
            painter.setFont(QFont("Arial", 7))
            painter.drawText(25, 50, "Barras")
            
        elif comp.type == 'xy_graph':
            # Gráfico XY
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(10, 10, 80, 30)
            # Eixos
            painter.drawLine(15, 35, 85, 35)  # X
            painter.drawLine(15, 15, 15, 35)  # Y
            # Linha de dados
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(15, 30, 40, 20)
            painter.drawLine(40, 20, 65, 25)
            painter.drawLine(65, 25, 80, 18)
            painter.setFont(QFont("Arial", 7))
            painter.drawText(35, 50, "X,Y")
            painter.drawLine(65, 25, 85, 18)
            
        elif comp.type == 'progress_bar':
            # Barra de progresso
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(10, 20, 80, 10)
            painter.setBrush(QBrush(QColor(0, 200, 0)))
            painter.drawRect(12, 22, 48, 6)  # 60% preenchido
            
        elif comp.type == 'gauge':
            # Indicador circular
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawEllipse(25, 10, 50, 30)
            # Ponteiro
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(50, 25, 65, 15)
            
        elif comp.type == 'icon':
            # Ícone/símbolo
            painter.setBrush(QBrush(QColor(255, 200, 0)))
            painter.setPen(QPen(QColor(200, 150, 0), 2))
            # Desenha símbolo de alerta
            polygon = QPolygon([QPoint(50, 10), QPoint(40, 30), QPoint(60, 30)])
            painter.drawPolygon(polygon)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawText(48, 26, "!")
            
    def mousePressEvent(self, event):
        """Componentes IHM não podem ser arrastados - apenas visualização"""
        # Componentes IHM são apenas para visualização na biblioteca
        # Eles serão adicionados através do editor IHM (clique direito no Display LADDER)
        if event.button() == Qt.LeftButton:
            print(f"ℹ️ Componente '{self.component.name}' selecionado")
            print("💡 Para adicionar componentes IHM:")
            print("   1. Arraste 'Display IHM' para o editor LADDER")
            print("   2. Clique direito no bloco Display")
            print("   3. Selecione 'Configurar IHM'")
        # Não inicia drag & drop

class IHMComponentLibrary(QWidget):
    """Biblioteca de componentes para IHM"""
    
    component_selected = pyqtSignal(object)
    add_component_requested = pyqtSignal(str, str)  # tipo, nome
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.create_components()
        
    def init_ui(self):
        """Inicializa interface da biblioteca"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        # Título
        title = QLabel("🖥️ Componentes IHM")
        title.setStyleSheet("""
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
        layout.addWidget(title)
        
        # Área de scroll para componentes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.components_widget = QWidget()
        self.components_layout = QVBoxLayout(self.components_widget)
        self.components_layout.setContentsMargins(2, 2, 2, 2)
        self.components_layout.setSpacing(2)
        
        scroll.setWidget(self.components_widget)
        layout.addWidget(scroll)
        
    def create_components(self):
        """Cria todos os componentes da biblioteca"""
        
        # Definir categorias e componentes - IHM OP320 Style
        categories = {
            "📝 Textos": {
                "color": "#4CAF50",
                "components": [
                    ("static_text", "Texto Estático", "Exibe texto fixo na tela"),
                    ("dynamic_text", "Texto Dinâmico", "Exibe valor de variável em tempo real")
                ]
            },
            "� Indicadores": {
                "color": "#FF9800",
                "components": [
                    ("led_indicator", "LED Indicador", "Indicador luminoso on/off com cores")
                ]
            },
            "� Entrada": {
                "color": "#2196F3", 
                "components": [
                    ("input_field", "Campo de Entrada", "Campo para inserir valores numéricos"),
                    ("function_button", "Botão de Função", "Botão mapeado para botão físico externo (F1-F4)")
                ]
            },
            "�️ Imagem": {
                "color": "#607D8B",
                "components": [
                    ("mono_image", "Área de Imagem", "Área para exibir imagens monocromáticas")
                ]
            },
            "� Gráficos": {
                "color": "#9C27B0",
                "components": [
                    ("bar_graph", "Gráfico de Barras", "Gráfico de barras para visualização de dados"),
                    ("xy_graph", "Gráfico X,Y", "Gráfico de linha/pontos para dados temporais")
                ]
            }
        }
        
        # Criar grupos de componentes
        for category_name, category_data in categories.items():
            self.create_category_group(category_name, category_data)
            
    def create_category_group(self, category_name, category_data):
        """Cria um grupo de categoria de componentes"""
        
        # Criar grupo
        group = QGroupBox(category_name)
        group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {category_data['color']};
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 8px;
                background-color: {category_data['color']};
                color: white;
                border-radius: 3px;
                margin-left: 5px;
            }}
        """)
        
        group_layout = QVBoxLayout(group)
        group_layout.setContentsMargins(5, 5, 5, 5)
        group_layout.setSpacing(2)
        
        # Adicionar componentes da categoria
        for comp_type, comp_name, comp_desc in category_data["components"]:
            component = IHMComponent(comp_name, comp_type, category_name)
            component.properties = {"description": comp_desc}
            
            # Criar botão para adicionar componente
            add_button = QPushButton(f"+ {comp_name}")
            add_button.setToolTip(f"Adicionar: {comp_name}\n{comp_desc}")
            add_button.setStyleSheet("""
                QPushButton {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    padding: 8px;
                    text-align: left;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                    border-color: #adb5bd;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
                }
            """)
            
            # Conectar sinal para adicionar componente
            add_button.clicked.connect(lambda checked, ct=comp_type, cn=comp_name: 
                                     self.request_add_component(ct, cn))
            
            group_layout.addWidget(add_button)
            
        self.components_layout.addWidget(group)
        
    def request_add_component(self, comp_type, comp_name):
        """Solicita adicionar componente ao canvas"""
        print(f"➕ Solicitação para adicionar: {comp_name} ({comp_type})")
        self.add_component_requested.emit(comp_type, comp_name)
        
    def get_component_by_type(self, comp_type):
        """Retorna dados do componente pelo tipo"""
        # Mapear tipos para criar novos componentes
        component_map = {
            "text": ("Texto Estático", "📝 Textos e Campos"),
            "input_field": ("Campo Entrada", "📝 Textos e Campos"),
            "label_var": ("Label Variável", "📝 Textos e Campos"),
            "status_text": ("Status Texto", "📝 Textos e Campos"),
            "button": ("Botão", "🔘 Botões e Controles"),
            "toggle_button": ("Botão Liga/Desliga", "🔘 Botões e Controles"),
            "momentary_button": ("Botão Momentâneo", "🔘 Botões e Controles"),
            "navigation_button": ("Botão Navegação", "🔘 Botões e Controles"),
            "indicator": ("LED Indicador", "💡 Indicadores"),
            "multi_state_indicator": ("Indicador Multi-Estado", "💡 Indicadores"),
            "alarm_indicator": ("Indicador Alarme", "💡 Indicadores"),
            "status_bar": ("Barra Status", "💡 Indicadores"),
            "bar_graph": ("Gráfico Barras", "📊 Gráficos"),
            "xy_graph": ("Gráfico XY", "📊 Gráficos"),
            "progress_bar": ("Barra Progresso", "📊 Gráficos"),
            "gauge": ("Indicador Circular", "📊 Gráficos"),
            "icon": ("Ícone/Símbolo", "🖼️ Elementos Visuais"),
            "line": ("Linha", "🖼️ Elementos Visuais"),
            "rectangle": ("Retângulo", "🖼️ Elementos Visuais"),
            "frame": ("Moldura", "🖼️ Elementos Visuais")
        }
        
        if comp_type in component_map:
            name, category = component_map[comp_type]
            return IHMComponent(name, comp_type, category)
        return None

# Widget de teste para desenvolvimento
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    library = IHMComponentLibrary()
    library.show()
    
    sys.exit(app.exec_())
#!/usr/bin/env python3
"""
Canvas LADDER - Editor Visual
Área de desenho para programação LADDER com drag & drop e conexões
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsProxyWidget, QMenu, QAction, QMessageBox, QGraphicsLineItem
)
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, QMimeData
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QDragEnterEvent,
    QDragMoveEvent, QDropEvent, QPalette
)

class LadderConnectionLine(QGraphicsItem):
    """Conexão LADDER real (horizontal + vertical, sem diagonal)"""
    
    def __init__(self, start_point, end_point):
        super().__init__()
        
        self.start_point = start_point
        self.end_point = end_point
        
        # Calcular pontos da conexão em L (horizontal + vertical)
        self.connection_points = self.calculate_ladder_path()
        
        # Estilo da linha LADDER
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(100)  # Acima do grid, abaixo dos componentes
        
    def calculate_ladder_path(self):
        """Calcula caminho em L da conexão LADDER"""
        start = self.start_point
        end = self.end_point
        
        # Conexão LADDER padrão: horizontal primeiro, depois vertical
        # Ponto intermediário para fazer o "L"
        intermediate = QPointF(end.x(), start.y())
        
        return [start, intermediate, end]
        
    def boundingRect(self):
        """Retorna retângulo delimitador da conexão"""
        points = self.connection_points
        if not points:
            return QRectF()
            
        # Encontrar limites
        min_x = min(p.x() for p in points)
        max_x = max(p.x() for p in points)
        min_y = min(p.y() for p in points)
        max_y = max(p.y() for p in points)
        
        # Adicionar margem para espessura da linha
        margin = 5
        return QRectF(min_x - margin, min_y - margin, 
                     max_x - min_x + 2*margin, max_y - min_y + 2*margin)
        
    def paint(self, painter, option, widget):
        """Desenha a conexão LADDER em formato L"""
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Cor baseada na seleção
        if self.isSelected():
            pen = QPen(QColor(0, 120, 212), 4)  # Azul quando selecionada
        else:
            pen = QPen(QColor(0, 0, 0), 3)      # Preta normal
            
        painter.setPen(pen)
        
        # Desenhar linhas do caminho em L
        points = self.connection_points
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            painter.drawLine(start, end)
        
        # Desenhar pontos de conexão nas extremidades
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        start = points[0]
        end = points[-1]
        
        # Pontos pequenos nas extremidades
        painter.drawEllipse(int(start.x()) - 2, int(start.y()) - 2, 4, 4)
        painter.drawEllipse(int(end.x()) - 2, int(end.y()) - 2, 4, 4)
        
        # Ponto de junção no meio (opcional)
        if len(points) > 2:
            junction = points[1]
            painter.drawEllipse(int(junction.x()) - 1, int(junction.y()) - 1, 2, 2)
    
    def update_path(self, start_point, end_point):
        """Atualiza o caminho da conexão"""
        self.start_point = start_point
        self.end_point = end_point
        self.connection_points = self.calculate_ladder_path()
        self.update()
        
    def contextMenuEvent(self, event):
        """Menu de contexto para conexão"""
        from PyQt5.QtWidgets import QMenu, QAction
        menu = QMenu()
        
        delete_action = QAction("🗑️ Excluir Conexão", menu)
        delete_action.triggered.connect(self.delete_connection)
        menu.addAction(delete_action)
        
        menu.exec_(event.screenPos())
        
    def delete_connection(self):
        """Exclui esta conexão"""
        # Encontrar o canvas pai e chamar método de exclusão
        scene = self.scene()
        if scene:
            for view in scene.views():
                parent = view.parent()
                if hasattr(parent, 'delete_connection'):
                    parent.delete_connection(self)
                    break

class LadderCanvasItem(QGraphicsItem):
    """Item no canvas LADDER com pontos de conexão"""
    
    def __init__(self, component_type, name, description, x=0, y=0):
        super().__init__()
        
        self.component_type = component_type
        self.name = name  
        self.description = description
        self.config = {}
        self.display_id = None  # Para componentes Display IHM
        self.ihm_config_data = {}  # Para armazenar configuração IHM específica
        
        # Configurações visuais - PADRÃO LADDER REAL
        self.width = 80   # Reduzido de 100 para 80
        self.height = 40  # Reduzido de 60 para 40
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        
        # PONTOS DE CONEXÃO LADDER - APENAS ENTRADA E SAÍDA
        self.connection_points = {
            'input': QPointF(0, self.height / 2),           # Entrada esquerda
            'output': QPointF(self.width, self.height / 2), # Saída direita
        }
        
        # Cores por tipo de componente
        self.colors = {
            'digital_input': QColor(40, 167, 69),    # Verde
            'analog_input': QColor(23, 162, 184),     # Azul claro
            'digital_output': QColor(220, 53, 69),    # Vermelho
            'timer': QColor(255, 193, 7),            # Amarelo
            'counter': QColor(111, 66, 193),         # Roxo
            'math': QColor(253, 126, 20),            # Laranja
            'comparator': QColor(32, 201, 151),      # Verde água
            'pid': QColor(232, 62, 140)              # Rosa
        }
        
    def get_connection_point(self, side):
        """Retorna ponto de conexão em coordenadas globais"""
        local_point = self.connection_points[side]
        return self.mapToScene(local_point)
        
    def get_closest_connection_point(self, scene_point):
        """Retorna o ponto de conexão mais próximo (input ou output)"""
        input_point = self.mapToScene(self.connection_points['input'])
        output_point = self.mapToScene(self.connection_points['output'])
        
        # Calcular distâncias
        input_distance = ((input_point.x() - scene_point.x()) ** 2 + 
                         (input_point.y() - scene_point.y()) ** 2) ** 0.5
        output_distance = ((output_point.x() - scene_point.x()) ** 2 + 
                          (output_point.y() - scene_point.y()) ** 2) ** 0.5
        
        # Retornar o mais próximo
        if input_distance < output_distance:
            return 'input'
        else:
            return 'output'
        
    def boundingRect(self):
        """Retorna retângulo delimitador"""
        return QRectF(0, 0, self.width, self.height)
        
    def paint(self, painter, option, widget):
        """Desenha o componente"""
        # Cor baseada no tipo
        color = self.colors.get(self.component_type, QColor(128, 128, 128))
        
        # Destacar se selecionado
        if self.isSelected():
            pen = QPen(QColor(0, 120, 212), 3)
            brush = QBrush(color.lighter(120))
        else:
            pen = QPen(color.darker(150), 2)
            brush = QBrush(color)
            
        painter.setPen(pen)
        painter.setBrush(brush)
        
        # Desenhar retângulo principal
        rect = QRectF(0, 0, self.width, self.height)
        painter.drawRoundedRect(rect, 5, 5)
        
        # Desenhar texto
        painter.setPen(QPen(Qt.black))
        
        # Tratamento especial para Display IHM - apenas nome
        if self.component_type == "DISPLAY_IHM":
            # Display IHM - mostrar nome configurado se disponível
            display_name = self.name  # Nome padrão
            
            # Se tem configuração IHM, usar o nome da tela configurada
            if hasattr(self, 'ihm_config_data') and self.ihm_config_data:
                if 'screen_name' in self.ihm_config_data:
                    display_name = self.ihm_config_data['screen_name']
            
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            text_rect = QRectF(0, 0, self.width, self.height)
            painter.drawText(text_rect, Qt.AlignCenter, display_name)
        else:
            # Outros componentes - nome + descrição
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            
            # Nome do componente
            name_rect = QRectF(0, 5, self.width, 20)
            painter.drawText(name_rect, Qt.AlignCenter, self.name)
            
            # Descrição
            painter.setFont(QFont("Arial", 8))
            desc_rect = QRectF(0, 25, self.width, 30)
            painter.drawText(desc_rect, Qt.AlignCenter | Qt.TextWordWrap, self.description)
        
        # Pontos de conexão LADDER (pequenos círculos brancos com borda preta)
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black, 2))
        
        # Desenhar todos os pontos de conexão
        for side, point in self.connection_points.items():
            # Círculo pequeno no ponto de conexão
            painter.drawEllipse(QRectF(point.x()-3, point.y()-3, 6, 6))
            
        # Destacar pontos se componente estiver selecionado
        if self.isSelected():
            painter.setBrush(QBrush(QColor(0, 120, 212)))
            painter.setPen(QPen(QColor(0, 120, 212), 2))
            for side, point in self.connection_points.items():
                painter.drawEllipse(QRectF(point.x()-4, point.y()-4, 8, 8))
        
    def mousePressEvent(self, event):
        """Evento de clique do mouse"""
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.screenPos())
        else:
            super().mousePressEvent(event)
            
    def show_context_menu(self, pos):
        """Mostra menu de contexto"""
        menu = QMenu()
        
        # Ações específicas para Display IHM
        if self.component_type == "DISPLAY_IHM":
            edit_action = menu.addAction("🖥️ Editar IHM")
            info_action = menu.addAction("ℹ️ Informações")
            menu.addSeparator()
            delete_action = menu.addAction("🗑️ Excluir")
            
            # Executar menu
            action = menu.exec_(pos)
            
            if action == edit_action:
                self.edit_ihm_configuration()
            elif action == info_action:
                self.show_ihm_info()
            elif action == delete_action:
                self.delete_component()
        else:
            # Menu padrão para outros componentes
            config_action = menu.addAction("⚙️ Configurar")
            delete_action = menu.addAction("🗑️ Excluir")
            copy_action = menu.addAction("📋 Copiar")
            
            # Executar menu
            action = menu.exec_(pos)
            
            if action == config_action:
                self.configure_component()
            elif action == delete_action:
                self.delete_component()
            elif action == copy_action:
                self.copy_component()
                
    def edit_ihm_configuration(self):
        """Abre editor IHM para este componente específico"""
        # Buscar o canvas pai e chamar o método de configuração
        scene = self.scene()
        if scene:
            # Encontrar o widget pai (LadderCanvas)
            for view in scene.views():
                parent_widget = view.parent()
                while parent_widget:
                    if hasattr(parent_widget, 'open_ihm_config_for_item'):
                        parent_widget.open_ihm_config_for_item(self)
                        return
                    parent_widget = parent_widget.parent()
        print("⚠️ Não foi possível encontrar o canvas LADDER para abrir configuração")
        
    def show_ihm_info(self):
        """Mostra informações do Display IHM"""
        from PyQt5.QtWidgets import QMessageBox
        
        config_info = ""
        if hasattr(self, 'ihm_config_data') and self.ihm_config_data:
            screen_count = len(self.ihm_config_data.get('screens', []))
            total_components = sum(len(s.get('components', [])) for s in self.ihm_config_data.get('screens', []))
            config_info = f"\n\n📊 Configuração atual:\n• {screen_count} tela(s)\n• {total_components} componente(s)"
        else:
            config_info = "\n\n⚠️ Ainda não configurado"
            
        QMessageBox.information(None, f"Display IHM - {self.name}", 
                              f"🖥️ {self.name}\n\n"
                              f"📱 Display ST7920 128x64 pixels\n"
                              f"🔧 Interface: SPI\n"
                              f"🎨 Tipo: Monocromático{config_info}\n\n"
                              f"💡 Clique direito → 'Editar IHM' para configurar")
            
    def configure_component(self):
        """Abre configuração do componente"""
        # TODO: Implementar diálogo de configuração
        QMessageBox.information(None, "Configurar", 
                               f"Configurar {self.name}\nTipo: {self.component_type}")
        
    def delete_component(self):
        """Remove componente do canvas"""
        if self.scene():
            self.scene().removeItem(self)
            
    def copy_component(self):
        """Copia componente"""
        # TODO: Implementar cópia
        QMessageBox.information(None, "Copiar", f"Componente {self.name} copiado")
        
    def itemChange(self, change, value):
        """Aplicar snap to grid quando item for movido e atualizar conexões"""
        # Use valor numérico da constante ItemPositionChange = 0
        if change == 0 and self.scene():  # ItemPositionChange
            # Obter referência ao canvas para usar o snap to grid
            canvas_widget = None
            if self.scene() and hasattr(self.scene(), 'views'):
                for view in self.scene().views():
                    parent = view.parent()
                    if hasattr(parent, 'snap_to_grid'):
                        canvas_widget = parent
                        break
            
            if canvas_widget and hasattr(value, 'x') and hasattr(value, 'y'):
                # Aplicar snap to grid
                snap_x, snap_y = canvas_widget.snap_to_grid(value.x(), value.y())
                snapped_pos = QPointF(snap_x, snap_y)
                
                # Atualizar conexões após movimento
                if hasattr(canvas_widget, 'update_connections_for_item'):
                    canvas_widget.update_connections_for_item(self)
                
                return snapped_pos
            
        return super().itemChange(change, value)


class LadderCanvas(QWidget):
    """Canvas principal para edição LADDER com grid automático e conexões"""
    
    component_selected = pyqtSignal(object)  # Emite quando componente é selecionado
    component_added = pyqtSignal(str, str)   # Emite quando componente é adicionado
    
    def __init__(self):
        super().__init__()
        
        # Configurações do GRID LADDER REAL - 10 COLUNAS COM ESPAÇOS PARA CONEXÕES
        self.BLOCKS_PER_ROW = 10     # 10 blocos por linha
        self.BLOCK_WIDTH = 80        # Largura de cada bloco  
        self.BLOCK_HEIGHT = 40       # Altura de cada bloco
        self.GRID_SPACING_X = 120    # Espaçamento horizontal maior para conexões (inclui margem)
        self.GRID_SPACING_Y = 60     # Espaçamento vertical maior para conexões (inclui margem)
        self.CANVAS_MARGIN = 20      # Margem das bordas
        
        # Espaços específicos para conexões LADDER
        self.CONNECTION_SPACE_X = 40 # Espaço horizontal entre blocos para linhas
        self.CONNECTION_SPACE_Y = 20 # Espaço vertical entre fileiras para linhas
        
        # Controle de posicionamento automático
        self.current_row = 0
        self.current_col = 0
        
        # SISTEMA DE CONEXÕES LADDER
        self.connection_mode = False          # Modo de criação de conexões
        self.connection_start_item = None     # Item de origem da conexão
        self.connection_start_point = None    # Ponto de origem
        self.temp_connection_line = None      # Linha temporária durante criação
        self.connections = []                 # Lista de todas as conexões
        
        self.init_ui()
        
        # Lista de componentes no canvas
        self.components = []
        
    def init_ui(self):
        """Inicializa interface do canvas"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título do canvas
        title_frame = QFrame()
        title_frame.setFixedHeight(40)
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #0078d4;
                border-bottom: 2px solid #005a9e;
            }
        """)
        
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("🎨 Editor LADDER - Canvas de Programação")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: white;")
        title_layout.addWidget(title)
        
        title_layout.addStretch()
        
        # Botão para modo de conexão
        from PyQt5.QtWidgets import QPushButton
        self.connection_button = QPushButton("🔗 Conectar")
        self.connection_button.setCheckable(True)
        self.connection_button.setFixedSize(100, 30)
        self.connection_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #dc3545;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:checked:hover {
                background-color: #c82333;
            }
        """)
        self.connection_button.clicked.connect(self.toggle_connection_mode)
        title_layout.addWidget(self.connection_button)
        
        # Informações do canvas
        info_label = QLabel("Arraste componentes da biblioteca para aqui")
        info_label.setFont(QFont("Arial", 9))
        info_label.setStyleSheet("color: #e6f3ff;")
        title_layout.addWidget(info_label)
        
        layout.addWidget(title_frame)
        
        # Área de desenho com scroll
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        
        # Configurar scene
        self.graphics_scene.setSceneRect(0, 0, 2000, 1500)  # Canvas grande
        self.graphics_scene.setBackgroundBrush(QBrush(QColor(250, 250, 250)))
        
        # Desenhar grid no fundo
        self.draw_grid()
        
        # Configurar view
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        
        # Habilitar drop
        self.graphics_view.setAcceptDrops(True)
        self.graphics_view.dragEnterEvent = self.drag_enter_event
        self.graphics_view.dragMoveEvent = self.drag_move_event  
        self.graphics_view.dropEvent = self.drop_event
        
        # Conectar eventos de mouse para conexões
        self.graphics_view.mousePressEvent = self.canvas_mouse_press_event
        
        # Conectar eventos de teclado para exclusão
        self.graphics_view.keyPressEvent = self.canvas_key_press_event
        
        # Configurar para capturar eventos de teclado
        self.setFocusPolicy(Qt.StrongFocus)
        self.graphics_view.setFocusPolicy(Qt.StrongFocus)
        
        layout.addWidget(self.graphics_view)
        
        # Barra de status do canvas
        status_frame = QFrame()
        status_frame.setFixedHeight(30)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("💡 DICA: Selecione conexões (linhas) e pressione DELETE para excluir")
        self.status_label.setFont(QFont("Arial", 9))
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.components_count = QLabel("Componentes: 0")
        self.components_count.setFont(QFont("Arial", 9))
        status_layout.addWidget(self.components_count)
        
        layout.addWidget(status_frame)
        
        # Conectar sinais
        self.graphics_scene.selectionChanged.connect(self.on_selection_changed)
        
        # Conectar eventos de teclado na scene também
        self.graphics_scene.keyPressEvent = self.scene_key_press_event
        
    def draw_grid(self):
        """Desenha grid LADDER no fundo do canvas com 10 colunas e espaços para conexões"""
        # Grid LADDER REAL - linhas de posicionamento dos blocos
        pen_main = QPen(QColor(150, 150, 150), 2)     # Linhas principais das colunas
        pen_guide = QPen(QColor(220, 220, 220), 1)    # Linhas guia horizontais
        pen_connection = QPen(QColor(200, 200, 200), 1)  # Linhas para conexões (pontilhada)
        
        scene_rect = self.graphics_scene.sceneRect()
        
        # Linhas verticais principais - delimitam as 10 colunas
        for col in range(self.BLOCKS_PER_ROW + 1):
            x = self.CANVAS_MARGIN + col * self.GRID_SPACING_X
            line = self.graphics_scene.addLine(x, 0, x, scene_rect.bottom(), pen_main)
            if line:
                line.setZValue(-1000)  # Enviar para trás
        
        # Linhas verticais de conexão (entre as colunas)
        for col in range(self.BLOCKS_PER_ROW):
            # Linha no meio entre duas colunas para mostrar onde fazer conexões
            x_center = self.CANVAS_MARGIN + col * self.GRID_SPACING_X + self.BLOCK_WIDTH + (self.CONNECTION_SPACE_X // 2)
            line = self.graphics_scene.addLine(x_center, 0, x_center, scene_rect.bottom(), pen_connection)
            if line:
                line.setZValue(-1000)
            
        # Linhas horizontais - delimitam as fileiras
        max_rows = int(scene_rect.bottom() / self.GRID_SPACING_Y) + 1
        for row in range(max_rows):
            y = self.CANVAS_MARGIN + row * self.GRID_SPACING_Y
            line = self.graphics_scene.addLine(0, y, scene_rect.right(), y, pen_guide)
            if line:
                line.setZValue(-1000)  # Enviar para trás
            
            # Linha horizontal de conexão (entre as fileiras)
            if row < max_rows - 1:
                y_center = y + self.BLOCK_HEIGHT + (self.CONNECTION_SPACE_Y // 2)
                line = self.graphics_scene.addLine(0, y_center, scene_rect.right(), y_center, pen_connection)
                if line:
                    line.setZValue(-1000)
            
        # Adicionar labels das colunas para facilitar visualização
        for col in range(self.BLOCKS_PER_ROW):
            x = self.CANVAS_MARGIN + col * self.GRID_SPACING_X + self.BLOCK_WIDTH // 2
            text_item = self.graphics_scene.addText(f"C{col+1}", QFont("Arial", 8))
            if text_item:
                text_item.setPos(x - 10, 5)
                text_item.setDefaultTextColor(QColor(120, 120, 120))
                text_item.setZValue(-999)
            
    def get_next_grid_position(self):
        """Calcula próxima posição no grid LADDER"""
        x = self.CANVAS_MARGIN + self.current_col * self.GRID_SPACING_X
        y = self.CANVAS_MARGIN + self.current_row * self.GRID_SPACING_Y
        
        # Avançar para próxima posição
        self.current_col += 1
        if self.current_col >= self.BLOCKS_PER_ROW:
            self.current_col = 0
            self.current_row += 1
            
        return x, y
        
    def snap_to_grid(self, x, y):
        """Ajusta coordenadas para o grid LADDER mais próximo"""
        # Calcular coluna e linha mais próximas
        col = round((x - self.CANVAS_MARGIN) / self.GRID_SPACING_X)
        row = round((y - self.CANVAS_MARGIN) / self.GRID_SPACING_Y)
        
        # Limitar aos limites do grid
        col = max(0, min(col, self.BLOCKS_PER_ROW - 1))
        row = max(0, row)
        
        # Calcular posição final
        snap_x = self.CANVAS_MARGIN + col * self.GRID_SPACING_X
        snap_y = self.CANVAS_MARGIN + row * self.GRID_SPACING_Y
        
        return snap_x, snap_y
    
    def toggle_connection_mode(self):
        """Ativa/desativa modo de conexão"""
        self.connection_mode = self.connection_button.isChecked()
        
        if self.connection_mode:
            self.connection_button.setText("🔗 Conectando")
            self.status_label.setText("MODO CONEXÃO: Clique em um componente para iniciar conexão")
            # Destacar pontos de conexão
            self.highlight_connection_points(True)
        else:
            self.connection_button.setText("🔗 Conectar")  
            self.status_label.setText("Selecione conexões e pressione DELETE para excluir | Arraste componentes")
            # Cancelar conexão em andamento
            self.cancel_current_connection()
            self.highlight_connection_points(False)
            
    def highlight_connection_points(self, highlight):
        """Destaca/remove destaque dos pontos de conexão"""
        for item in self.graphics_scene.items():
            if isinstance(item, LadderCanvasItem):
                item.update()  # Força redesenho com/sem destaque
                
    def cancel_current_connection(self):
        """Cancela conexão atual"""
        if self.temp_connection_line:
            self.graphics_scene.removeItem(self.temp_connection_line)
            self.temp_connection_line = None
        self.connection_start_item = None
        self.connection_start_point = None
        
    def create_connection(self, start_item, start_point, end_item, end_point):
        """Cria uma conexão LADDER entre dois componentes"""
        start_pos = start_item.get_connection_point(start_point)
        end_pos = end_item.get_connection_point(end_point)
        
        # Criar conexão LADDER em formato L (horizontal + vertical)
        connection = LadderConnectionLine(start_pos, end_pos)
        self.graphics_scene.addItem(connection)
        
        # Armazenar informações da conexão
        connection_data = {
            'line': connection,
            'start_item': start_item,
            'start_point': start_point,
            'end_item': end_item,
            'end_point': end_point,
            'type': 'ladder_L'
        }
        
        self.connections.append(connection_data)
        
        print(f"🔗 Conexão LADDER criada: {start_item.name}({start_point}) → {end_item.name}({end_point})")
        return connection
        
    def update_connections_for_item(self, item):
        """Atualiza posições das conexões quando um item se move"""
        for conn_data in self.connections:
            if conn_data['start_item'] == item or conn_data['end_item'] == item:
                # Recalcular posições
                start_pos = conn_data['start_item'].get_connection_point(conn_data['start_point'])
                end_pos = conn_data['end_item'].get_connection_point(conn_data['end_point'])
                
                # Atualizar caminho da conexão LADDER
                conn_data['line'].update_path(start_pos, end_pos)
    
    def canvas_mouse_press_event(self, event):
        """Trata cliques no canvas para criar conexões"""
        if self.connection_mode and event.button() == Qt.LeftButton:
            # Encontrar item clicado
            scene_pos = self.graphics_view.mapToScene(event.pos())
            item = self.graphics_scene.itemAt(scene_pos, self.graphics_view.transform())
            
            if isinstance(item, LadderCanvasItem):
                if self.connection_start_item is None:
                    # Primeiro clique - iniciar conexão
                    self.connection_start_item = item
                    self.connection_start_point = item.get_closest_connection_point(scene_pos)
                    self.status_label.setText(f"Clique no destino para conectar com {item.name}")
                    print(f"🔗 Iniciando conexão em {item.name}({self.connection_start_point})")
                    
                else:
                    # Segundo clique - finalizar conexão
                    if item != self.connection_start_item:
                        end_point = item.get_closest_connection_point(scene_pos)
                        
                        # Criar conexão
                        self.create_connection(
                            self.connection_start_item, self.connection_start_point,
                            item, end_point
                        )
                        
                        self.status_label.setText(f"Conexão criada! Clique em outro componente para nova conexão")
                    else:
                        self.status_label.setText("Não é possível conectar um componente a ele mesmo")
                    
                    # Reset para nova conexão
                    self.connection_start_item = None
                    self.connection_start_point = None
            else:
                # Clique no vazio - cancelar conexão atual
                if self.connection_start_item:
                    self.connection_start_item = None
                    self.connection_start_point = None
                    self.status_label.setText("Conexão cancelada - Clique em um componente para iniciar")
        else:
            # Modo normal - comportamento padrão
            from PyQt5.QtWidgets import QGraphicsView
            QGraphicsView.mousePressEvent(self.graphics_view, event)
    
    def canvas_key_press_event(self, event):
        """Tratamento de teclas no canvas - incluindo Delete para conexões"""
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
        else:
            # Comportamento padrão para outras teclas
            from PyQt5.QtWidgets import QGraphicsView
            QGraphicsView.keyPressEvent(self.graphics_view, event)
    
    def scene_key_press_event(self, event):
        """Tratamento de teclas na scene - incluindo Delete para conexões"""
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
        else:
            # Comportamento padrão para outras teclas
            from PyQt5.QtWidgets import QGraphicsScene
            QGraphicsScene.keyPressEvent(self.graphics_scene, event)
    
    def keyPressEvent(self, event):
        """Tratamento de teclas - incluindo Delete para conexões"""
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
        else:
            super().keyPressEvent(event)
            
    def delete_selected_items(self):
        """Exclui itens selecionados (componentes e conexões)"""
        selected_items = self.graphics_scene.selectedItems()
        if not selected_items:
            return
            
        deleted_components = 0
        deleted_connections = 0
        
        for item in selected_items:
            if isinstance(item, LadderCanvasItem):
                # Excluir componente e suas conexões
                self.delete_component_and_connections(item)
                deleted_components += 1
                
            elif isinstance(item, LadderConnectionLine):
                # Excluir apenas a conexão
                self.delete_connection(item)
                deleted_connections += 1
                
        if deleted_components > 0 or deleted_connections > 0:
            msg = f"🗑️ Excluídos: {deleted_components} componente(s), {deleted_connections} conexão(ões)"
            self.status_label.setText(msg)
            print(msg)
    
    def delete_connection(self, connection_line):
        """Exclui uma conexão específica"""
        # Encontrar e remover da lista de conexões
        for i, conn_data in enumerate(self.connections):
            if conn_data['line'] == connection_line:
                # Remover da cena
                self.graphics_scene.removeItem(connection_line)
                # Remover da lista
                del self.connections[i]
                print(f"🗑️ Conexão removida")
                break
                
    def delete_component_and_connections(self, component):
        """Exclui um componente e todas suas conexões"""
        # Primeiro, excluir todas as conexões do componente
        connections_to_remove = []
        for conn_data in self.connections:
            if conn_data['start_item'] == component or conn_data['end_item'] == component:
                connections_to_remove.append(conn_data)
        
        # Remover conexões
        for conn_data in connections_to_remove:
            self.graphics_scene.removeItem(conn_data['line'])
            self.connections.remove(conn_data)
            
        # Remover componente da cena
        self.graphics_scene.removeItem(component)
        
        # Remover da lista de componentes
        if component in self.components:
            self.components.remove(component)
            
        print(f"🗑️ Componente {component.name} e suas conexões removidos")
            
    def drag_enter_event(self, event):
        """Evento de entrada do drag"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.status_label.setText("Posicione o componente no canvas...")
            
    def drag_move_event(self, event):
        """Evento de movimento do drag"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def drop_event(self, event):
        """Evento de drop - adiciona componente ao canvas no próximo slot do grid"""
        if event.mimeData().hasText():
            # Extrair dados do componente
            component_data = event.mimeData().text()
            parts = component_data.split('|')
            
            if len(parts) >= 3:
                component_type = parts[0]
                name = parts[1]
                description = parts[2]
                
                # USAR GRID AUTOMÁTICO - não mais posição do mouse
                x, y = self.get_next_grid_position()
                
                # Criar item no canvas com tamanho padronizado
                item = LadderCanvasItem(component_type, name, description, x, y)
                
                # Aplicar tamanho fixo do grid
                item.width = self.BLOCK_WIDTH
                item.height = self.BLOCK_HEIGHT
                
                self.graphics_scene.addItem(item)
                
                # Adicionar à lista
                self.components.append(item)
                
                # Verificar se é um Display IHM - abrir configuração automaticamente
                if component_type == "DISPLAY_IHM":
                    # Gerar ID único para este display
                    display_count = sum(1 for comp in self.components if comp.component_type == "DISPLAY_IHM")
                    unique_id = f"Display_{display_count}"
                    item.display_id = unique_id
                    item.name = unique_id  # Atualizar nome para ser único
                    
                    print(f"🖥️ Display IHM '{unique_id}' adicionado ao LADDER na posição ({x}, {y}) - abrindo configuração...")
                    
                    # Abrir configuração automaticamente (com delay para garantir que o item foi adicionado)
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(100, lambda: self.open_ihm_config_for_item(item))
                
                # Atualizar status
                self.update_status()
                
                # Emitir sinal
                self.component_added.emit(component_type, name)
                
                event.acceptProposedAction()
                
    def on_selection_changed(self):
        """Chamado quando seleção muda"""
        selected_items = self.graphics_scene.selectedItems()
        
        if selected_items:
            item = selected_items[0]
            # Verificar se é LadderCanvasItem (que tem os atributos)
            if hasattr(item, 'name') and hasattr(item, 'component_type'):
                self.status_label.setText(f"Selecionado: {item.name} ({item.component_type})")
                self.component_selected.emit(item)
            else:
                self.status_label.setText("Item gráfico selecionado")
                self.component_selected.emit(None)
        else:
            self.status_label.setText("Nenhum componente selecionado")
            self.component_selected.emit(None)
            
    def update_status(self):
        """Atualiza status do canvas"""
        count = len(self.components)
        self.components_count.setText(f"Componentes: {count}")
        
        if count == 0:
            self.status_label.setText("Pronto - Arraste componentes para começar")
        else:
            self.status_label.setText(f"Canvas com {count} componente(s)")
            
    def clear_canvas(self):
        """Limpa todos os componentes do canvas"""
        self.graphics_scene.clear()
        self.components.clear()
        self.draw_grid()  # Redesenhar grid
        self.update_status()
        
    def get_component_count_by_type(self):
        """Retorna contagem de componentes por tipo"""
        count = {}
        for component in self.components:
            comp_type = component.component_type
            count[comp_type] = count.get(comp_type, 0) + 1
        return count
        
    def export_to_python(self):
        """Exporta canvas para código Python (futuro)"""
        # TODO: Implementar geração de código
        code_lines = [
            "# Código gerado automaticamente pelo CLP-IHM-PICO",
            "# Raspberry Pi Pico - MicroPython",
            "",
            "from machine import Pin, PWM, ADC",
            "import utime",
            "",
        ]
        
        # Analisar componentes e gerar código
        component_counts = self.get_component_count_by_type()
        
        for comp_type, count in component_counts.items():
            code_lines.append(f"# {comp_type}: {count} instância(s)")
            
        return "\n".join(code_lines)
        
    def open_ihm_config_for_item(self, ihm_item):
        """Abre configuração IHM específica para um item"""
        try:
            from ihm_config_dialog import IHMConfigDialog
            
            print(f"🖥️ Abrindo configuração para {ihm_item.name}...")
            
            # Criar dialog com configuração específica deste item
            dialog = IHMConfigDialog(self)
            
            # Se há configuração salva para este item, carregar
            if hasattr(ihm_item, 'ihm_config_data') and ihm_item.ihm_config_data:
                print(f"📁 Carregando configuração salva de {ihm_item.name}")
                dialog.load_saved_data(ihm_item.ihm_config_data)
            
            # Conectar salvamento para este item específico
            dialog.finished.connect(lambda result: self.save_ihm_config_for_item(ihm_item, dialog) if result else None)
            
            # Exibir dialog
            dialog.exec_()
            
        except ImportError as e:
            print(f"❌ Erro ao abrir configuração IHM: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erro", 
                              f"Não foi possível abrir a configuração IHM:\n{e}")
            
    def save_ihm_config_for_item(self, ihm_item, dialog):
        """Salva configuração IHM específica para um item"""
        if hasattr(dialog, 'get_screen_data'):
            # Obter dados da tela única configurada
            screen_data = dialog.get_screen_data()
            
            # Criar estrutura de configuração compatível
            config_data = {
                'screen_name': screen_data['name'],
                'components': screen_data['components'],
                'properties': screen_data.get('properties', {
                    'background_color': 'light_green',
                    'timeout': 0,
                    'show_header': True
                })
            }
            
            # Salvar no item específico
            ihm_item.ihm_config_data = config_data
            print(f"💾 Configuração IHM salva para {ihm_item.name}")
            print(f"📊 Tela: '{screen_data['name']}' com {len(screen_data['components'])} componente(s)")
            
            # Atualizar visual do item
            ihm_item.update()
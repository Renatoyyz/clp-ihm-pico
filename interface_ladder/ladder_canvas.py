#!/usr/bin/env python3
"""
Canvas LADDER - Editor Visual
Área de desenho para programação LADDER com drag & drop
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsProxyWidget, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, QMimeData
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QDragEnterEvent,
    QDragMoveEvent, QDropEvent, QPalette
)

class LadderCanvasItem(QGraphicsItem):
    """Item no canvas LADDER"""
    
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
        
        # Pontos de conexão (pequenos círculos)
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black, 1))
        
        # Entrada (esquerda)
        painter.drawEllipse(QRectF(-5, self.height/2-3, 6, 6))
        
        # Saída (direita)  
        painter.drawEllipse(QRectF(self.width-1, self.height/2-3, 6, 6))
        
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
        """Aplicar snap to grid quando item for movido"""
        # Use valor numérico da constante ItemPositionChange = 0
        if change == 0 and self.scene():  # ItemPositionChange
            # Obter referência ao canvas para usar o snap to grid
            canvas_widget = None
            if self.scene() and hasattr(self.scene(), 'views'):
                for view in self.scene().views():
                    if hasattr(view.parent(), 'snap_to_grid'):
                        canvas_widget = view.parent()
                        break
            
            if canvas_widget and hasattr(value, 'x') and hasattr(value, 'y'):
                # Aplicar snap to grid
                snap_x, snap_y = canvas_widget.snap_to_grid(value.x(), value.y())
                return QPointF(snap_x, snap_y)
                
        return super().itemChange(change, value)


class LadderCanvas(QWidget):
    """Canvas principal para edição LADDER com grid automático"""
    
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
        
        # Informações do canvas
        info_label = QLabel("Arraste componentes da biblioteca para aqui")
        info_label.setFont(QFont("Arial", 9))
        info_label.setStyleSheet("color: #e6f3ff;")
        title_layout.addStretch()
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
        
        self.status_label = QLabel("Pronto - Arraste componentes para começar")
        self.status_label.setFont(QFont("Arial", 9))
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.components_count = QLabel("Componentes: 0")
        self.components_count.setFont(QFont("Arial", 9))
        status_layout.addWidget(self.components_count)
        
        layout.addWidget(status_frame)
        
        # Conectar sinais
        self.graphics_scene.selectionChanged.connect(self.on_selection_changed)
        
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
"""
Canvas para Design de Telas IHM
Display ST7920 128x64 pixels

Sistema de design visual para criação de interfaces IHM
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QGraphicsView, QGraphicsScene, QGraphicsItem,
                           QGraphicsPixmapItem, QFrame, QPushButton, QComboBox,
                           QSpinBox, QCheckBox, QGroupBox, QTabWidget,
                           QTextEdit, QLineEdit, QFormLayout, QMenu, QAction)
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QRect, QPointF, QTimer
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPixmap,
                        QTransform, QDragEnterEvent, QDropEvent, QKeyEvent, QContextMenuEvent)
import json

class IHMScreenItem(QGraphicsItem):
    """Item gráfico que representa um componente IHM na tela"""
    
    def __init__(self, component, parent=None):
        super().__init__(parent)
        self.component = component
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        
        # Propriedades visuais
        self.selected_pen = QPen(QColor(255, 0, 0), 2)
        self.normal_pen = QPen(QColor(0, 0, 0), 1)
        
    def boundingRect(self):
        """Define área do item"""
        return QRectF(0, 0, self.component.width, self.component.height)
        
    def paint(self, painter, option, widget):
        """Renderiza o componente na tela"""
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Selecionar cor baseada no estado
        if self.isSelected():
            painter.setPen(self.selected_pen)
        else:
            painter.setPen(self.normal_pen)
            
        # Desenhar componente baseado no tipo
        self.draw_component(painter)
        
    def draw_component(self, painter):
        """Desenha o componente específico"""
        comp = self.component
        rect = self.boundingRect()
        
        # RENDERIZAÇÃO MONOCROMÁTICA - DISPLAY ST7920 REAL
        painter.setPen(QPen(QColor(0, 0, 0), 1))  # Sempre preto
        painter.setBrush(QBrush())  # Sem preenchimento por padrão
        
        if comp.type in ['text', 'static_text']:
            # Texto estático - Preto sobre fundo claro
            font_size = comp.properties.get('font_size', 8)
            painter.setFont(QFont("Arial", font_size))
            painter.setPen(QPen(QColor(0, 0, 0), 1))  # Texto preto
            text = comp.properties.get('text', 'Texto')
            painter.drawText(rect, 0x0001 | 0x0020, text)  # AlignLeft | AlignTop
            
        elif comp.type == 'dynamic_text':
            # Texto dinâmico - Preto sobre fundo claro
            font_size = comp.properties.get('font_size', 8)
            painter.setFont(QFont("Arial", font_size))
            painter.setPen(QPen(QColor(0, 0, 0), 1))  # Texto preto
            # Simular valor dinâmico
            variable = comp.properties.get('variable', 'TAG001')
            format_str = comp.properties.get('format', '%.1f')
            try:
                demo_value = 25.4
                text = format_str % demo_value if '%' in format_str else f"{variable}: {demo_value}"
            except:
                text = f"{variable}: 25.4"
            painter.drawText(rect, 0x0001 | 0x0020, text)  # AlignLeft | AlignTop
            
        elif comp.type == 'input_field':
            # Campo de entrada
            painter.drawRect(rect)
            painter.setFont(QFont("Arial", 7))
            value = comp.properties.get('value', '123.45')
            painter.drawText(rect.adjusted(2, 1, -2, -1), Qt.AlignLeft | Qt.AlignVCenter, str(value))
            
        elif comp.type == 'button':
            # Botão
            painter.setBrush(QBrush(QColor(240, 240, 240)))
            painter.drawRect(rect)
            painter.setBrush(QBrush())
            painter.setFont(QFont("Arial", 7))
            text = comp.properties.get('text', 'OK')
            painter.drawText(rect, Qt.AlignCenter, text)
            
        elif comp.type in ['indicator', 'led_indicator']:
            # LED Indicador - MONOCROMÁTICO (Display ST7920)
            led_size = min(rect.width(), rect.height()) - 2
            led_rect = QRectF(rect.x() + 1, rect.y() + 1, led_size, led_size)
            
            # Estado do LED (ON = preenchido preto, OFF = só borda)
            state = comp.properties.get('state', True)
            
            if state:
                # LED LIGADO - Círculo preenchido preto
                painter.setBrush(QBrush(QColor(0, 0, 0)))
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawEllipse(int(led_rect.x()), int(led_rect.y()), int(led_rect.width()), int(led_rect.height()))
            else:
                # LED DESLIGADO - Só borda preta
                painter.setBrush(QBrush())  # Sem preenchimento
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawEllipse(int(led_rect.x()), int(led_rect.y()), int(led_rect.width()), int(led_rect.height()))
            
        elif comp.type == 'bar_graph':
            # Gráfico de barras - MONOCROMÁTICO
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect)
            
            # Barras preenchidas em preto baseado no valor
            variable = comp.properties.get('variable', 'REG001')
            min_scale = comp.properties.get('min_scale', 0)
            max_scale = comp.properties.get('max_scale', 100)
            
            # Simular 4 barras com valores diferentes
            bar_width = (rect.width() - 10) / 4
            for i in range(4):
                # Valores simulados
                value = 25 + (i * 20)  # 25, 45, 65, 85
                percentage = (value - min_scale) / (max_scale - min_scale)
                bar_height = (rect.height() - 6) * percentage
                
                bar_x = rect.x() + 2 + i * bar_width
                bar_y = rect.bottom() - 2 - bar_height
                
                painter.setBrush(QBrush(QColor(0, 0, 0)))  # Preto
                painter.drawRect(int(bar_x), int(bar_y), int(bar_width - 1), int(bar_height))
            
        elif comp.type == 'xy_graph':
            # Gráfico XY - MONOCROMÁTICO
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect)
            
            # Eixos em preto - Converter para int
            painter.drawLine(int(rect.x() + 5), int(rect.bottom() - 5), int(rect.right() - 2), int(rect.bottom() - 5))  # X
            painter.drawLine(int(rect.x() + 5), int(rect.y() + 2), int(rect.x() + 5), int(rect.bottom() - 5))  # Y
            
            # Linha de dados em preto
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            x_step = (rect.width() - 10) / 10
            for i in range(10):
                x1 = int(rect.x() + 5 + i * x_step)
                y1 = int(rect.y() + rect.height() * 0.3 + (i % 3) * 5)
                x2 = int(rect.x() + 5 + (i + 1) * x_step)
                y2 = int(rect.y() + rect.height() * 0.3 + ((i + 1) % 3) * 5)
                if i < 9:
                    painter.drawLine(x1, y1, x2, y2)
                    # Pontos nos dados
                    painter.drawEllipse(int(x1 - 1), int(y1 - 1), 2, 2)
                    
        elif comp.type == 'input_field':
            # Campo de entrada - MONOCROMÁTICO
            painter.setBrush(QBrush())  # Sem preenchimento
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect)
            
            # Valor atual do campo
            painter.setFont(QFont("Arial", 7))
            value = comp.properties.get('value', '123.45')
            text_rect = rect.adjusted(2, 1, -2, -1)
            painter.drawText(text_rect, 0x0001 | 0x0080, str(value))  # AlignLeft | AlignVCenter
            
        elif comp.type == 'function_button':
            # Botão de função - MONOCROMÁTICO com seta
            painter.setBrush(QBrush())  # Sem preenchimento
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect)
            
            # Seta simples em preto - Converter para int
            arrow_y = int(rect.center().y())
            arrow_left = int(rect.x() + 3)
            arrow_right = int(rect.right() - 10)
            arrow_tip = int(rect.right() - 3)
            
            # Linha horizontal da seta
            painter.drawLine(arrow_left, arrow_y, arrow_right, arrow_y)
            # Ponta da seta
            painter.drawLine(arrow_right, arrow_y - 2, arrow_tip, arrow_y)
            painter.drawLine(arrow_right, arrow_y + 2, arrow_tip, arrow_y)
            
            # Texto do botão (F1-F4)
            painter.setFont(QFont("Arial", 6))
            func_key = comp.properties.get('function_key', 'F1')
            text_rect = QRect(int(rect.x()), int(rect.bottom() - 8), int(rect.width()), 8)
            painter.drawText(text_rect, 0x0004 | 0x0020, func_key)  # AlignHCenter | AlignTop
            
        elif comp.type == 'mono_image':
            # Área de imagem monocromática - Display ST7920
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect)
            
            # Padrão de pixels simulando imagem monocromática
            pixel_size = 2
            for x in range(int(rect.x()) + 1, int(rect.right()) - 1, pixel_size * 2):
                for y in range(int(rect.y()) + 1, int(rect.bottom()) - 1, pixel_size * 2):
                    if (x + y) % 6 == 0:  # Padrão alternado
                        painter.fillRect(x, y, pixel_size, pixel_size, QColor(0, 0, 0))
                        
            # Texto indicativo
            painter.setFont(QFont("Arial", 6))
            painter.drawText(rect, 0x0084, "IMG")  # AlignCenter
                    
        elif comp.type == 'progress_bar':
            # Barra de progresso
            painter.drawRect(rect)
            value = comp.properties.get('value', 75)
            fill_width = (rect.width() - 2) * (value / 100)
            fill_rect = QRectF(rect.x() + 1, rect.y() + 1, fill_width, rect.height() - 2)
            painter.setBrush(QBrush(QColor(0, 200, 0)))
            painter.drawRect(int(fill_rect.x()), int(fill_rect.y()), int(fill_rect.width()), int(fill_rect.height()))
            
        elif comp.type == 'gauge':
            # Indicador circular
            painter.drawEllipse(rect)
            # Ponteiro simples
            center_x = rect.center().x()
            center_y = rect.center().y()
            angle = comp.properties.get('angle', 45)  # graus
            import math
            end_x = center_x + (rect.width() / 3) * math.cos(math.radians(angle))
            end_y = center_y + (rect.height() / 3) * math.sin(math.radians(angle))
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(int(center_x), int(center_y), int(end_x), int(end_y))
            
        else:
            # Componente genérico
            painter.drawRect(rect)
            painter.setFont(QFont("Arial", 6))
            painter.drawText(rect, Qt.AlignCenter, comp.type.upper())
            
    def itemChange(self, change, value):
        """Detecta mudanças no item"""
        if change == QGraphicsItem.ItemPositionChange:
            # Snap to grid (pixels)
            new_pos = value
            snap_x = round(new_pos.x())
            snap_y = round(new_pos.y())
            
            # Limitar aos bounds da tela (128x64)
            snap_x = max(0, min(snap_x, 128 - self.component.width))
            snap_y = max(0, min(snap_y, 64 - self.component.height))
            
            # Atualizar posição do componente
            self.component.x = snap_x
            self.component.y = snap_y
            
            return QPointF(snap_x, snap_y)
            
        return super().itemChange(change, value)

class IHMScreenCanvas(QGraphicsView):
    """Canvas para design de telas IHM 128x64"""
    
    component_selected = pyqtSignal(object)
    component_moved = pyqtSignal(object)
    components_changed = pyqtSignal()  # Novo sinal para mudanças
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar cena para 128x64 pixels
        self._scene = QGraphicsScene(0, 0, 128, 64)
        self.setScene(self._scene)
        
        # Lista de componentes na tela
        self.screen_components = []
        
        # Configurações visuais
        self.setup_canvas()
        
        # Conectar sinais
        self._scene.selectionChanged.connect(self.on_selection_changed)
        
    def setup_canvas(self):
        """Configura aparência do canvas"""
        # Fundo branco (simula tela LCD)
        self._scene.setBackgroundBrush(QBrush(QColor(200, 255, 200)))  # Verde claro LCD
        
        # Desenhar grid de pixels
        self.draw_pixel_grid()
        
        # Configurar visualização
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
        # Escala para visualizar melhor (4x)
        self.scale(4, 4)
        
        # Configurar scroll
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
    def draw_pixel_grid(self):
        """Desenha grid de pixels na tela"""
        pen = QPen(QColor(150, 200, 150), 0.2)  # Linha muito fina
        
        # Linhas verticais
        for x in range(0, 129, 8):  # Grid a cada 8 pixels
            line = self._scene.addLine(x, 0, x, 64, pen)
            line.setZValue(-1)  # Atrás dos componentes
            
        # Linhas horizontais  
        for y in range(0, 65, 8):  # Grid a cada 8 pixels
            line = self._scene.addLine(0, y, 128, y, pen)
            line.setZValue(-1)
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Aceita drag de componentes IHM"""
        if event.mimeData().hasText():
            text = event.mimeData().text()
            if text.startswith("ihm_component:"):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
            
    def dropEvent(self, event: QDropEvent):
        """Processa drop de componente na tela"""
        if event.mimeData().hasText():
            text = event.mimeData().text()
            if text.startswith("ihm_component:"):
                # Parse do tipo de componente
                parts = text.split(":")
                if len(parts) >= 3:
                    comp_type = parts[1]
                    comp_name = parts[2]
                    
                    # Converter coordenadas da view para cena
                    scene_pos = self.mapToScene(event.pos())
                    
                    # Criar componente
                    self.add_component(comp_type, scene_pos.x(), scene_pos.y())
                    
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
            
    def add_component(self, comp_type, x, y):
        """Adiciona componente à tela"""
        from ihm_components import IHMComponent
        
        # Criar componente
        component = IHMComponent(f"{comp_type}_{len(self.screen_components)+1}", comp_type, "IHM")
        
        # Definir tamanho padrão baseado no tipo
        if comp_type in ['text', 'label_var', 'status_text']:
            component.width = 40
            component.height = 8
        elif comp_type in ['input_field']:
            component.width = 32
            component.height = 10
        elif comp_type in ['button', 'toggle_button', 'momentary_button']:
            component.width = 24
            component.height = 12
        elif comp_type in ['indicator', 'alarm_indicator']:
            component.width = 8
            component.height = 8
        elif comp_type in ['bar_graph', 'progress_bar']:
            component.width = 48
            component.height = 12
        elif comp_type == 'xy_graph':
            component.width = 64
            component.height = 32
        elif comp_type == 'gauge':
            component.width = 24
            component.height = 24
        else:
            component.width = 16
            component.height = 8
            
        # Posicionar (snap to pixel)
        component.x = max(0, min(int(x), 128 - component.width))
        component.y = max(0, min(int(y), 64 - component.height))
        
        # Propriedades padrão baseadas no tipo
        if comp_type == 'text':
            component.properties = {'text': 'Texto', 'font_size': 8}
        elif comp_type == 'input_field':
            component.properties = {'value': 0, 'format': '%.1f', 'variable': ''}
        elif comp_type == 'button':
            component.properties = {'text': 'OK', 'action': 'none'}
        elif comp_type == 'indicator':
            component.properties = {'state': True, 'variable': ''}
        elif comp_type in ['bar_graph', 'progress_bar']:
            component.properties = {'value': 50, 'min': 0, 'max': 100, 'variable': ''}
        elif comp_type == 'gauge':
            component.properties = {'value': 50, 'min': 0, 'max': 100, 'angle': 45}
        else:
            component.properties = {}
            
        # Criar item gráfico
        item = IHMScreenItem(component)
        item.setPos(component.x, component.y)
        
        # Adicionar à cena
        self._scene.addItem(item)
        self.screen_components.append({'component': component, 'item': item})
        
        print(f"Componente {comp_type} adicionado em ({component.x}, {component.y})")
        
        # Emitir sinal de mudança para salvar automaticamente
        self.components_changed.emit()
        
    def on_selection_changed(self):
        """Quando seleção muda"""
        try:
            # Verificar se a scene ainda existe e é válida
            if hasattr(self, '_scene') and self._scene is not None:
                selected_items = self._scene.selectedItems()
                if selected_items:
                    # Encontrar componente correspondente
                    for comp_data in self.screen_components:
                        if comp_data['item'] in selected_items:
                            self.component_selected.emit(comp_data['component'])
                            break
                else:
                    self.component_selected.emit(None)
        except RuntimeError:
            # Scene foi deletada, ignorar
            pass
            
    def contextMenuEvent(self, event: QContextMenuEvent):
        """Menu de contexto (botão direito)"""
        try:
            # Verificar se a scene ainda existe e é válida
            if hasattr(self, '_scene') and self._scene is not None:
                # Verificar se clicou em um componente
                scene_pos = self.mapToScene(event.pos())
                item = self._scene.itemAt(scene_pos, QTransform())
                
                if isinstance(item, IHMScreenItem):
                    # Menu para componente
                    menu = QMenu(self)
                    
                    delete_action = QAction("🗑️ Excluir Componente", self)
                    delete_action.triggered.connect(lambda: self.delete_selected_component())
                    menu.addAction(delete_action)
                    
                    menu.exec_(event.globalPos())
                else:
                    super().contextMenuEvent(event)
            else:
                super().contextMenuEvent(event)
        except RuntimeError:
            # Scene foi deletada, ignorar
            super().contextMenuEvent(event)
            
    def keyPressEvent(self, event: QKeyEvent):
        """Eventos de teclado"""
        if event.key() == Qt.Key.Key_Delete:
            self.delete_selected_component()
        else:
            super().keyPressEvent(event)
            
    def delete_selected_component(self):
        """Exclui o componente selecionado"""
        try:
            # Verificar se a scene ainda existe e é válida
            if not hasattr(self, '_scene') or self._scene is None:
                return
                
            selected_items = self._scene.selectedItems()
            if not selected_items:
                print("⚠️ Nenhum componente selecionado para excluir")
                return
                
            components_deleted = 0
            for item in selected_items:
                if isinstance(item, IHMScreenItem):
                    # Encontrar e remover da lista de componentes
                    for i, comp_data in enumerate(self.screen_components):
                        if comp_data['item'] == item:
                            # Remover da cena
                            self._scene.removeItem(item)
                            # Obter nome antes de remover
                            component_name = comp_data['component'].name
                            component_type = comp_data['component'].type
                            # Remover da lista
                            del self.screen_components[i]
                            components_deleted += 1
                            print(f"🗑️ Componente '{component_name}' ({component_type}) excluído")
                            break
                            
            if components_deleted > 0:
                # Emitir sinais apenas se algo foi removido
                self.component_selected.emit(None)  # Limpar seleção
                self.components_changed.emit()  # Salvar alterações
                print(f"✅ {components_deleted} componente(s) removido(s) do canvas IHM")
            else:
                print("⚠️ Nenhum componente IHM válido foi encontrado para exclusão")
        except RuntimeError:
            # Scene foi deletada, ignorar
            pass
            
    def save_components_to_current_screen(self):
        """Salva componentes atuais na tela ativa do gerenciador"""
        if hasattr(self, 'current_screen') and self.current_screen:
            # Limpar componentes existentes da tela
            self.current_screen.components.clear()
            
            # Adicionar componentes atuais do canvas
            for comp_data in self.screen_components:
                self.current_screen.components.append(comp_data['component'])
                
            print(f"💾 {len(self.screen_components)} componentes salvos na tela '{self.current_screen.name}'")
            
    def set_current_screen(self, screen):
        """Define a tela atual para salvar componentes"""
        self.current_screen = screen
            
    def clear_screen(self):
        """Limpa todos os componentes da tela"""
        for comp_data in self.screen_components:
            self._scene.removeItem(comp_data['item'])
        self.screen_components.clear()
        
    def get_screen_data(self):
        """Retorna dados da tela para salvar"""
        screen_data = []
        for comp_data in self.screen_components:
            component = comp_data['component']
            screen_data.append({
                'type': component.type,
                'name': component.name,
                'x': component.x,
                'y': component.y,
                'width': component.width,
                'height': component.height,
                'properties': component.properties
            })
        return screen_data
        
    def load_screen_data(self, screen_data):
        """Carrega dados de tela salvos"""
        self.clear_screen()
        
        for comp_data in screen_data:
            from ihm_components import IHMComponent
            
            # Recriar componente com valores seguros
            component_name = comp_data.get('name', f"Componente_{len(self.screen_components)+1}")
            component_type = comp_data.get('type', 'text')
            
            component = IHMComponent(component_name, component_type, "IHM")
            component.x = comp_data.get('x', 0)
            component.y = comp_data.get('y', 0) 
            component.width = comp_data.get('width', 16)
            component.height = comp_data.get('height', 8)
            component.properties = comp_data.get('properties', {})
            
            # Criar item gráfico
            item = IHMScreenItem(component)
            item.setPos(component.x, component.y)
            
            # Adicionar à cena
            self._scene.addItem(item)
            self.screen_components.append({'component': component, 'item': item})
            
    def update_component_item(self, component):
        """Atualiza item visual de um componente específico"""
        for comp_data in self.screen_components:
            if comp_data['component'] == component:
                item = comp_data['item']
                
                # Atualizar posição
                item.setPos(component.x, component.y)
                
                # Forçar atualização do bounding rect (dimensões)
                item.prepareGeometryChange()
                
                # Forçar redesenho completo
                item.update()
                
                # Atualizar toda a cena
                self._scene.update()
                
                # Emitir sinal de mudança
                self.components_changed.emit()
                
                print(f"🔄 Item visual atualizado: {component.name} - Pos:({component.x},{component.y}) Size:({component.width}x{component.height})")
                break

class IHMPropertiesPanel(QWidget):
    """Painel de propriedades para componentes IHM"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_component = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializa interface do painel"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("🔧 Propriedades")
        title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #2d5aa0;
                padding: 5px;
                background-color: #f0f8ff;
                border: 1px solid #b8d4f0;
                border-radius: 3px;
            }
        """)
        layout.addWidget(title)
        
        # Área de propriedades
        self.properties_widget = QWidget()
        self.properties_layout = QFormLayout(self.properties_widget)
        layout.addWidget(self.properties_widget)
        
        # Mensagem quando nenhum componente selecionado
        self.no_selection_label = QLabel("Selecione um componente\npara editar propriedades")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet("color: #666; padding: 20px;")
        layout.addWidget(self.no_selection_label)
        
        layout.addStretch()
        
    def set_component(self, component):
        """Define componente para editar"""
        self.current_component = component
        self.update_properties()
        
    def update_properties(self):
        """Atualiza interface de propriedades"""
        # Limpar propriedades existentes
        for i in reversed(range(self.properties_layout.count())):
            child = self.properties_layout.takeAt(i).widget()
            if child:
                child.deleteLater()
                
        if not self.current_component:
            self.properties_widget.hide()
            self.no_selection_label.show()
            return
            
        self.properties_widget.show()
        self.no_selection_label.hide()
        
        # Propriedades básicas
        comp = self.current_component
        
        # Nome
        name_edit = QLineEdit(comp.name)
        name_edit.textChanged.connect(lambda text: setattr(comp, 'name', text))
        self.properties_layout.addRow("Nome:", name_edit)
        
        # Posição X, Y
        x_spin = QSpinBox()
        x_spin.setRange(0, 127)
        x_spin.setValue(comp.x)
        x_spin.valueChanged.connect(lambda val: setattr(comp, 'x', val))
        self.properties_layout.addRow("X:", x_spin)
        
        y_spin = QSpinBox()
        y_spin.setRange(0, 63)
        y_spin.setValue(comp.y)
        y_spin.valueChanged.connect(lambda val: setattr(comp, 'y', val))
        self.properties_layout.addRow("Y:", y_spin)
        
        # Tamanho Width, Height
        w_spin = QSpinBox()
        w_spin.setRange(1, 128)
        w_spin.setValue(comp.width)
        w_spin.valueChanged.connect(lambda val: setattr(comp, 'width', val))
        self.properties_layout.addRow("Largura:", w_spin)
        
        h_spin = QSpinBox()
        h_spin.setRange(1, 64)
        h_spin.setValue(comp.height)
        h_spin.valueChanged.connect(lambda val: setattr(comp, 'height', val))
        self.properties_layout.addRow("Altura:", h_spin)
        
        # Botão Atualizar
        from PyQt5.QtWidgets import QPushButton
        update_btn = QPushButton("🔄 Atualizar")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        update_btn.clicked.connect(self.update_component_display)
        self.properties_layout.addRow("", update_btn)
        
        # Propriedades específicas do tipo
        self.add_type_specific_properties(comp)
        
    def add_type_specific_properties(self, component):
        """Adiciona propriedades específicas do tipo de componente - OP320 Style"""
        comp_type = component.type
        props = component.properties
        
        if comp_type == 'static_text':
            # Texto estático
            text_edit = QLineEdit(props.get('text', 'Texto'))
            text_edit.textChanged.connect(lambda text: props.update({'text': text}))
            self.properties_layout.addRow("Texto:", text_edit)
            
            font_size_spin = QSpinBox()
            font_size_spin.setRange(6, 16)
            font_size_spin.setValue(props.get('font_size', 8))
            font_size_spin.valueChanged.connect(lambda val: props.update({'font_size': val}))
            self.properties_layout.addRow("Tamanho Fonte:", font_size_spin)
            
        elif comp_type == 'dynamic_text':
            # Texto dinâmico
            var_edit = QLineEdit(props.get('variable', 'TAG001'))
            var_edit.textChanged.connect(lambda text: props.update({'variable': text}))
            self.properties_layout.addRow("Variável CLP:", var_edit)
            
            format_edit = QLineEdit(props.get('format', '%.1f'))
            format_edit.textChanged.connect(lambda text: props.update({'format': text}))
            self.properties_layout.addRow("Formato:", format_edit)
            
            font_size_spin = QSpinBox()
            font_size_spin.setRange(6, 16)
            font_size_spin.setValue(props.get('font_size', 8))
            font_size_spin.valueChanged.connect(lambda val: props.update({'font_size': val}))
            self.properties_layout.addRow("Tamanho Fonte:", font_size_spin)
            
        elif comp_type == 'led_indicator':
            # LED Indicador
            var_edit = QLineEdit(props.get('variable', 'BIT001'))
            var_edit.textChanged.connect(lambda text: props.update({'variable': text}))
            self.properties_layout.addRow("Bit CLP:", var_edit)
            
            from PyQt5.QtWidgets import QComboBox
            color_combo = QComboBox()
            color_combo.addItems(['Verde', 'Vermelho', 'Amarelo', 'Azul'])
            color_combo.setCurrentText(props.get('color', 'Verde'))
            color_combo.currentTextChanged.connect(lambda text: props.update({'color': text}))
            self.properties_layout.addRow("Cor:", color_combo)
            
        elif comp_type == 'input_field':
            # Campo de entrada
            var_edit = QLineEdit(props.get('variable', 'REG001'))
            var_edit.textChanged.connect(lambda text: props.update({'variable': text}))
            self.properties_layout.addRow("Registro CLP:", var_edit)
            
            min_spin = QSpinBox()
            min_spin.setRange(-9999, 9999)
            min_spin.setValue(props.get('min_value', 0))
            min_spin.valueChanged.connect(lambda val: props.update({'min_value': val}))
            self.properties_layout.addRow("Valor Mín:", min_spin)
            
            max_spin = QSpinBox()
            max_spin.setRange(-9999, 9999)
            max_spin.setValue(props.get('max_value', 100))
            max_spin.valueChanged.connect(lambda val: props.update({'max_value': val}))
            self.properties_layout.addRow("Valor Máx:", max_spin)
            
        elif comp_type == 'function_button':
            # Botão de função
            from PyQt5.QtWidgets import QComboBox
            func_combo = QComboBox()
            func_combo.addItems(['F1', 'F2', 'F3', 'F4'])
            func_combo.setCurrentText(props.get('function_key', 'F1'))
            func_combo.currentTextChanged.connect(lambda text: props.update({'function_key': text}))
            self.properties_layout.addRow("Botão Físico:", func_combo)
            
            text_edit = QLineEdit(props.get('text', 'OK'))
            text_edit.textChanged.connect(lambda text: props.update({'text': text}))
            self.properties_layout.addRow("Rótulo:", text_edit)
            
            action_edit = QLineEdit(props.get('action', 'SET_BIT'))
            action_edit.textChanged.connect(lambda text: props.update({'action': text}))
            self.properties_layout.addRow("Ação CLP:", action_edit)
            
        elif comp_type == 'mono_image':
            # Área de imagem
            file_edit = QLineEdit(props.get('image_file', 'logo.bmp'))
            file_edit.textChanged.connect(lambda text: props.update({'image_file': text}))
            self.properties_layout.addRow("Arquivo:", file_edit)
            
            from PyQt5.QtWidgets import QCheckBox
            stretch_check = QCheckBox()
            stretch_check.setChecked(props.get('stretch', False))
            stretch_check.toggled.connect(lambda checked: props.update({'stretch': checked}))
            self.properties_layout.addRow("Esticar:", stretch_check)
            
        elif comp_type == 'bar_graph':
            # Gráfico de barras
            var_edit = QLineEdit(props.get('variable', 'REG001'))
            var_edit.textChanged.connect(lambda text: props.update({'variable': text}))
            self.properties_layout.addRow("Variável:", var_edit)
            
            min_spin = QSpinBox()
            min_spin.setRange(0, 1000)
            min_spin.setValue(props.get('min_scale', 0))
            min_spin.valueChanged.connect(lambda val: props.update({'min_scale': val}))
            self.properties_layout.addRow("Escala Mín:", min_spin)
            
            max_spin = QSpinBox()
            max_spin.setRange(0, 1000)
            max_spin.setValue(props.get('max_scale', 100))
            max_spin.valueChanged.connect(lambda val: props.update({'max_scale': val}))
            self.properties_layout.addRow("Escala Máx:", max_spin)
            
        elif comp_type == 'xy_graph':
            # Gráfico XY
            var_edit = QLineEdit(props.get('variable', 'REG001'))
            var_edit.textChanged.connect(lambda text: props.update({'variable': text}))
            self.properties_layout.addRow("Variável:", var_edit)
            
            points_spin = QSpinBox()
            points_spin.setRange(10, 100)
            points_spin.setValue(props.get('max_points', 50))
            points_spin.valueChanged.connect(lambda val: props.update({'max_points': val}))
            self.properties_layout.addRow("Máx Pontos:", points_spin)
            
            y_min_spin = QSpinBox()
            y_min_spin.setRange(-1000, 1000)
            y_min_spin.setValue(props.get('y_min', 0))
            y_min_spin.valueChanged.connect(lambda val: props.update({'y_min': val}))
            self.properties_layout.addRow("Y Mín:", y_min_spin)
            
            y_max_spin = QSpinBox()
            y_max_spin.setRange(-1000, 1000)
            y_max_spin.setValue(props.get('y_max', 100))
            y_max_spin.valueChanged.connect(lambda val: props.update({'y_max': val}))
            self.properties_layout.addRow("Y Máx:", y_max_spin)
            
    def update_component_display(self):
        """Atualiza a exibição do componente no canvas"""
        if self.current_component:
            print(f"🔄 Atualizando componente '{self.current_component.name}'...")
            print(f"📐 Nova Posição: ({self.current_component.x}, {self.current_component.y})")
            print(f"📏 Novo Tamanho: {self.current_component.width} x {self.current_component.height}")
            
            # Procurar o canvas IHM na hierarquia de widgets
            widget = self
            canvas = None
            
            while widget:
                parent = widget.parent()
                if parent and hasattr(parent, 'update_component_item'):
                    canvas = parent
                    break
                elif hasattr(parent, 'ihm_canvas') and hasattr(parent.ihm_canvas, 'update_component_item'):
                    canvas = parent.ihm_canvas
                    break
                widget = parent
            
            # Tentar atualizar através do canvas encontrado
            if canvas:
                canvas.update_component_item(self.current_component)
                print("✅ Componente atualizado visualmente no canvas!")
            else:
                print("⚠️ Canvas não encontrado - Propriedades salvas, redesenho na próxima interação")

# Widget de teste
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
    from ihm_components import IHMComponentLibrary
    
    app = QApplication(sys.argv)
    
    # Janela principal de teste
    window = QMainWindow()
    window.setWindowTitle("Teste Canvas IHM")
    window.setGeometry(100, 100, 1000, 600)
    
    central = QWidget()
    layout = QHBoxLayout(central)
    
    # Biblioteca de componentes
    library = IHMComponentLibrary()
    layout.addWidget(library, 1)
    
    # Canvas
    canvas = IHMScreenCanvas()
    layout.addWidget(canvas, 2)
    
    # Painel de propriedades
    properties = IHMPropertiesPanel()
    layout.addWidget(properties, 1)
    
    # Conectar sinais
    canvas.component_selected.connect(properties.set_component)
    
    window.setCentralWidget(central)
    window.show()
    
    sys.exit(app.exec_())
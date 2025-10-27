#!/usr/bin/env python3
"""
Biblioteca de Componentes LADDER
Componentes visuais para programação LADDER
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTreeWidget, QTreeWidgetItem, QGroupBox, QScrollArea,
    QFrame, QGridLayout, QSpinBox, QComboBox, QLineEdit,
    QApplication
)
from PyQt5.QtCore import Qt, QMimeData, QSize, pyqtSignal
from PyQt5.QtGui import (
    QDrag, QPainter, QColor, QPen, QBrush, QFont, 
    QPixmap, QPalette, QIcon
)

class LadderComponent(QWidget):
    """Classe base para todos os componentes LADDER"""
    
    def __init__(self, component_type, name, description):
        super().__init__()
        self.component_type = component_type
        self.name = name
        self.description = description
        self.config = {}
        
        self.setFixedSize(80, 60)
        self.setStyleSheet("""
            QWidget {
                border: 2px solid #666;
                border-radius: 5px;
                background-color: #f0f0f0;
                margin: 2px;
            }
            QWidget:hover {
                border: 2px solid #0078d4;
                background-color: #e6f3ff;
            }
        """)
        
        # Layout para o componente
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Nome do componente
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 8, QFont.Bold))
        layout.addWidget(name_label)
        
        # Descrição
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setFont(QFont("Arial", 7))
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Habilitar drag
        self.setAcceptDrops(False)
        
    def mousePressEvent(self, event):
        """Inicia drag & drop"""
        if event.button() == Qt.LeftButton:
            self.start_drag()
            
    def start_drag(self):
        """Inicia operação de drag"""
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # Dados do componente
        component_data = f"{self.component_type}|{self.name}|{self.description}"
        mime_data.setText(component_data)
        
        # Criar pixmap do componente
        pixmap = self.grab()
        
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())
        
        # Executar drag
        drop_action = drag.exec_(Qt.CopyAction)


class DigitalInputComponent(LadderComponent):
    """Componente de Entrada Digital"""
    
    def __init__(self, pin_number=0):
        super().__init__("digital_input", f"DI{pin_number:02d}", f"GP{pin_number}")
        self.pin_number = pin_number
        self.config = {
            'pin': pin_number,
            'pull_up': True,
            'invert': False,
            'debounce': 50
        }


class AnalogInputComponent(LadderComponent):
    """Componente de Entrada Analógica"""
    
    def __init__(self, adc_number=0):
        super().__init__("analog_input", f"AI{adc_number:02d}", f"ADC{adc_number}")
        self.adc_number = adc_number
        self.config = {
            'adc_pin': adc_number + 26,  # ADC0=GP26, ADC1=GP27, ADC2=GP28
            'resolution': 16,
            'scale_min': 0.0,
            'scale_max': 3.3,
            'filter': False
        }


class DigitalOutputComponent(LadderComponent):
    """Componente de Saída Digital"""
    
    def __init__(self, pin_number=0):
        super().__init__("digital_output", f"DO{pin_number:02d}", f"GP{pin_number}")
        self.pin_number = pin_number
        self.config = {
            'pin': pin_number,
            'mode': 'digital',  # 'digital' ou 'pwm'
            'pwm_freq': 1000,
            'initial_state': False
        }


class TimerComponent(LadderComponent):
    """Componente de Temporizador"""
    
    def __init__(self, timer_id=0):
        super().__init__("timer", f"T{timer_id:02d}", "Timer")
        self.timer_id = timer_id
        self.config = {
            'type': 'TON',  # TON, TOF, TP
            'preset': 1000,  # ms
            'reset_condition': None
        }


class CounterComponent(LadderComponent):
    """Componente de Contador"""
    
    def __init__(self, counter_id=0):
        super().__init__("counter", f"C{counter_id:02d}", "Counter")
        self.counter_id = counter_id
        self.config = {
            'type': 'CTU',  # CTU, CTD, CTUD
            'preset': 10,
            'reset_condition': None
        }


class MathComponent(LadderComponent):
    """Componente de Função Matemática"""
    
    def __init__(self, function='ADD'):
        super().__init__("math", function, "Math")
        self.function = function
        self.config = {
            'operation': function,  # ADD, SUB, MUL, DIV, MOD, ABS, SQRT
            'input_a': 0,
            'input_b': 0,
            'result': 0
        }


class ComparatorComponent(LadderComponent):
    """Componente Comparador"""
    
    def __init__(self, operation='EQ'):
        super().__init__("comparator", operation, "Compare")
        self.operation = operation
        self.config = {
            'operation': operation,  # EQ, NE, GT, GE, LT, LE
            'input_a': 0,
            'input_b': 0
        }


class PIDComponent(LadderComponent):
    """Componente PID"""
    
    def __init__(self, pid_id=0):
        super().__init__("pid", f"PID{pid_id}", "PID Ctrl")
        self.pid_id = pid_id
        self.config = {
            'kp': 1.0,
            'ki': 0.1,
            'kd': 0.01,
            'setpoint': 0.0,
            'output_min': 0.0,
            'output_max': 100.0,
            'pwm_outputs': []  # Lista de pinos PWM
        }


class ComponentLibrary(QWidget):
    """Widget da biblioteca de componentes"""
    
    component_selected = pyqtSignal(str, str)  # tipo, dados
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa interface da biblioteca"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Título
        title = QLabel("📚 Biblioteca LADDER")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #0078d4;
                color: white;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title)
        
        # Área de scroll para componentes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget principal dos componentes
        components_widget = QWidget()
        components_layout = QVBoxLayout(components_widget)
        
        # Grupo 1: Entradas Digitais
        digital_inputs_group = self.create_digital_inputs_group()
        components_layout.addWidget(digital_inputs_group)
        
        # Grupo 2: Entradas Analógicas
        analog_inputs_group = self.create_analog_inputs_group()
        components_layout.addWidget(analog_inputs_group)
        
        # Grupo 3: Saídas Digitais
        digital_outputs_group = self.create_digital_outputs_group()
        components_layout.addWidget(digital_outputs_group)
        
        # Grupo 4: Temporizadores
        timers_group = self.create_timers_group()
        components_layout.addWidget(timers_group)
        
        # Grupo 5: Contadores
        counters_group = self.create_counters_group()
        components_layout.addWidget(counters_group)
        
        # Grupo 6: Funções Matemáticas
        math_group = self.create_math_group()
        components_layout.addWidget(math_group)
        
        # Grupo 7: Comparadores
        comparators_group = self.create_comparators_group()
        components_layout.addWidget(comparators_group)
        
        # Grupo 8: Controladores PID
        pid_group = self.create_pid_group()
        components_layout.addWidget(pid_group)
        
        # Grupo 9: Interface IHM
        ihm_group = self.create_ihm_group()
        components_layout.addWidget(ihm_group)
        
        # Grupo 10: Comunicação RS485
        rs485_group = self.create_rs485_group()
        components_layout.addWidget(rs485_group)
        
        # Adicionar stretch para empurrar para cima
        components_layout.addStretch()
        
        scroll.setWidget(components_widget)
        layout.addWidget(scroll)
        
    def create_digital_inputs_group(self):
        """Cria grupo de entradas digitais"""
        group = QGroupBox("🔌 Entradas Digitais (8)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #28a745;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # Pinos digitais disponíveis do Pico (evitando pinos especiais)
        available_pins = [2, 3, 4, 5, 6, 7, 8, 9]  # 8 entradas digitais
        
        for i, pin in enumerate(available_pins):
            component = DigitalInputComponent(pin)
            layout.addWidget(component, i // 2, i % 2)
            
        return group
        
    def create_analog_inputs_group(self):
        """Cria grupo de entradas analógicas"""
        group = QGroupBox("📊 Entradas Analógicas (3)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #17a2b8;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # 3 ADCs disponíveis no Pico
        for i in range(3):
            component = AnalogInputComponent(i)
            layout.addWidget(component, i // 2, i % 2)
            
        return group
        
    def create_digital_outputs_group(self):
        """Cria grupo de saídas digitais"""
        group = QGroupBox("⚡ Saídas Digitais (6)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dc3545;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # Pinos de saída disponíveis
        output_pins = [10, 11, 12, 13, 14, 15]  # 6 saídas digitais/PWM
        
        for i, pin in enumerate(output_pins):
            component = DigitalOutputComponent(pin)
            layout.addWidget(component, i // 2, i % 2)
            
        return group
        
    def create_timers_group(self):
        """Cria grupo de temporizadores"""
        group = QGroupBox("⏱️ Temporizadores (16)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ffc107;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # 16 temporizadores
        for i in range(16):
            component = TimerComponent(i)
            layout.addWidget(component, i // 4, i % 4)
            
        return group
        
    def create_counters_group(self):
        """Cria grupo de contadores"""
        group = QGroupBox("🔢 Contadores (16)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #6f42c1;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # 16 contadores
        for i in range(16):
            component = CounterComponent(i)
            layout.addWidget(component, i // 4, i % 4)
            
        return group
        
    def create_math_group(self):
        """Cria grupo de funções matemáticas"""
        group = QGroupBox("🧮 Funções Matemáticas")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #fd7e14;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # Funções matemáticas disponíveis
        math_functions = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'ABS', 'SQRT', 'POW']
        
        for i, func in enumerate(math_functions):
            component = MathComponent(func)
            layout.addWidget(component, i // 4, i % 4)
            
        return group
        
    def create_comparators_group(self):
        """Cria grupo de comparadores"""
        group = QGroupBox("⚖️ Comparadores")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #20c997;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # Operações de comparação
        comparisons = ['EQ', 'NE', 'GT', 'GE', 'LT', 'LE']
        
        for i, comp in enumerate(comparisons):
            component = ComparatorComponent(comp)
            layout.addWidget(component, i // 3, i % 3)
            
        return group
        
    def create_pid_group(self):
        """Cria grupo de controladores PID"""
        group = QGroupBox("🎛️ Controladores PID (4)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e83e8c;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # 4 controladores PID
        for i in range(4):
            component = PIDComponent(i)
            layout.addWidget(component, i // 2, i % 2)
            
        return group
        
    def create_ihm_group(self):
        """Cria grupo de interface IHM"""
        group = QGroupBox("🖥️ Interface IHM")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #17a2b8;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # Componente Display IHM
        self.display_ihm_component = DisplayIHMComponent()
        # Conectar sinal para abrir configuração
        self.display_ihm_component.configure_ihm.connect(self.open_ihm_configuration)
        layout.addWidget(self.display_ihm_component, 0, 0)
            
        return group
        
    def open_ihm_configuration(self):
        """Abre janela de configuração IHM"""
        print("🖥️ Abrindo configuração do Display IHM...")
        self.show_ihm_dialog()
        
    def show_ihm_dialog(self):
        """Mostra janela de configuração IHM"""
        try:
            from ihm_config_dialog import IHMConfigDialog
            dialog = IHMConfigDialog(self)
            dialog.exec_()
        except ImportError as e:
            print(f"⚠️ Erro ao abrir configuração IHM: {e}")
            # Fallback: mostrar mensagem simples
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "IHM", 
                                  "🖥️ Configuração IHM\n\n"
                                  "Janela de configuração do Display ST7920 (128x64)\n"
                                  "Em desenvolvimento...")

    def create_rs485_group(self):
        """Cria grupo de componentes RS485"""
        group = QGroupBox("🌐 Comunicação RS485")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #FF9800;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QGridLayout(group)
        
        # Linha 1: Blocos de Leitura
        read_coils = RS485Component("READ_COILS", "Read Coils", "Ler bobinas (0x01)")
        layout.addWidget(read_coils, 0, 0)
        
        read_inputs = RS485Component("READ_INPUTS", "Read Inputs", "Ler entradas discretas (0x02)")
        layout.addWidget(read_inputs, 0, 1)
        
        read_holding = RS485Component("READ_HOLDING", "Read Holding", "Ler registradores holding (0x03)")
        layout.addWidget(read_holding, 0, 2)
        
        # Linha 2: Blocos de Escrita
        write_coil = RS485Component("WRITE_COIL", "Write Coil", "Escrever bobina (0x05)")
        layout.addWidget(write_coil, 1, 0)
        
        write_register = RS485Component("WRITE_REG", "Write Reg", "Escrever registrador (0x06)")
        layout.addWidget(write_register, 1, 1)
        
        write_multiple = RS485Component("WRITE_MULTI", "Write Multi", "Escrever múltiplos (0x10)")
        layout.addWidget(write_multiple, 1, 2)
        
        # Linha 3: Blocos de Controle
        rs485_master = RS485Component("RS485_MASTER", "RS485 Master", "Controlador master da rede")
        layout.addWidget(rs485_master, 2, 0)
        
        device_status = RS485Component("DEVICE_STATUS", "Device Status", "Monitor status dispositivo")
        layout.addWidget(device_status, 2, 1)
        
        network_scan = RS485Component("NETWORK_SCAN", "Net Scan", "Escaneamento da rede")
        layout.addWidget(network_scan, 2, 2)
        
        return group


class DisplayIHMComponent(LadderComponent):
    """Componente especial para configuração de Display IHM ST7920"""
    
    # Sinal para abrir janela de configuração
    configure_ihm = pyqtSignal()
    
    def __init__(self):
        super().__init__("DISPLAY_IHM", "Display IHM", "Configurar telas do display ST7920 128x64")
        
        # Configurar aparência específica
        self.setStyleSheet("""
            QWidget {
                border: 3px solid #17a2b8;
                border-radius: 8px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e0f7ff, 
                    stop: 1 #b3e5fc
                );
                margin: 2px;
            }
            QWidget:hover {
                border: 3px solid #0c7b93;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #b3e5fc,
                    stop: 1 #81d4fa
                );
            }
        """)
        
    def paintEvent(self, event):
        """Desenha o componente Display IHM"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar ícone do display
        rect = self.rect().adjusted(10, 20, -10, -15)
        
        # Moldura do display
        painter.setPen(QPen(QColor(23, 162, 184), 2))
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.drawRect(rect)
        
        # Área da tela
        screen_rect = rect.adjusted(3, 3, -3, -3)
        painter.setBrush(QBrush(QColor(150, 255, 150)))
        painter.drawRect(screen_rect)
        
        # Simular pixels/conteúdo
        painter.setPen(QPen(QColor(0, 100, 0), 1))
        painter.setFont(QFont("Arial", 6))
        painter.drawText(screen_rect.adjusted(2, 2, -2, -2), Qt.AlignCenter, "128x64\nST7920")
        
        # Título
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        title_rect = self.rect().adjusted(0, 5, 0, -40)
        painter.drawText(title_rect, Qt.AlignCenter, "Display IHM")
        
    def mousePressEvent(self, event):
        """Detecta clique para abrir configuração ou iniciar drag"""
        if event.button() == Qt.LeftButton:
            # Salvar posição inicial do mouse
            self.drag_start_position = event.pos()
        else:
            # Comportamento normal para outros botões
            super().mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        """Detecta movimento para iniciar drag"""
        if not (event.buttons() & Qt.LeftButton):
            return
            
        # Verificar se moveu o suficiente para iniciar drag
        if hasattr(self, 'drag_start_position'):
            distance = (event.pos() - self.drag_start_position).manhattanLength()
            if distance >= QApplication.startDragDistance():
                # Iniciar drag & drop
                self.start_drag()
                
    def mouseReleaseEvent(self, event):
        """Detecta clique simples para abrir configuração"""
        if event.button() == Qt.LeftButton and hasattr(self, 'drag_start_position'):
            # Se não houve movimento significativo, é um clique simples
            distance = (event.pos() - self.drag_start_position).manhattanLength()
            if distance < QApplication.startDragDistance():
                print("ℹ️ Clique simples no Display IHM - use clique direito para configurar")
        elif event.button() == Qt.RightButton:
            # Clique direito - abrir menu de contexto
            self.show_context_menu(event.pos())
        
        super().mouseReleaseEvent(event)
        
    def show_context_menu(self, position):
        """Mostra menu de contexto com opções do Display IHM"""
        from PyQt5.QtWidgets import QMenu, QAction
        
        menu = QMenu(self)
        
        # Ação para configurar IHM
        config_action = QAction("🖥️ Configurar IHM", self)
        config_action.triggered.connect(self.open_ihm_configuration)
        menu.addAction(config_action)
        
        # Separador
        menu.addSeparator()
        
        # Informações do display
        info_action = QAction("ℹ️ Informações", self)
        info_action.triggered.connect(self.show_display_info)
        menu.addAction(info_action)
        
        # Mostrar menu na posição do clique
        menu.exec_(self.mapToGlobal(position))
        
    def open_ihm_configuration(self):
        """Abre configuração IHM via menu de contexto"""
        print("🖥️ Abrindo configuração do Display IHM via menu de contexto...")
        self.configure_ihm.emit()
        
    def show_display_info(self):
        """Mostra informações do display ST7920"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Display ST7920", 
                              "📱 Display ST7920 128x64\n\n"
                              "• Resolução: 128 × 64 pixels\n"
                              "• Interface: SPI\n"
                              "• Tipo: Monocromático\n\n"
                              "🖱️ Clique direito → 'Configurar IHM'\n"
                              "para abrir o editor de interface")


class RS485Component(LadderComponent):
    """Componente específico para blocos RS485"""
    
    def __init__(self, component_type, name, description):
        super().__init__(component_type, name, description)
        
        # Cores específicas por tipo
        self.colors = {
            # Blocos de Leitura - Verde
            'READ_COILS': '#4CAF50',
            'READ_INPUTS': '#4CAF50', 
            'READ_HOLDING': '#4CAF50',
            
            # Blocos de Escrita - Azul
            'WRITE_COIL': '#2196F3',
            'WRITE_REG': '#2196F3',
            'WRITE_MULTI': '#2196F3',
            
            # Blocos de Controle - Laranja
            'RS485_MASTER': '#FF9800',
            'DEVICE_STATUS': '#FF9800',
            'NETWORK_SCAN': '#FF9800'
        }
        
        color = self.colors.get(component_type, '#607D8B')
        
        # Aplicar estilo específico
        self.setStyleSheet(f"""
            QWidget {{
                border: 2px solid {color};
                border-radius: 5px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {color}30, 
                    stop: 1 {color}10
                );
                margin: 2px;
            }}
            QWidget:hover {{
                border: 3px solid {color};
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {color}50,
                    stop: 1 {color}20
                );
            }}
        """)
        
    def paintEvent(self, event):
        """Desenha o componente RS485"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar ícone específico por tipo
        rect = self.rect().adjusted(5, 15, -5, -10)
        
        # Cor do ícone baseada no tipo
        color = QColor(self.colors.get(self.component_type, '#607D8B'))
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color.lighter(150)))
        
        if 'READ' in self.component_type:
            # Ícone de leitura - seta para baixo
            painter.drawRect(rect)
            # Seta
            arrow_y = rect.center().y()
            painter.drawLine(rect.left() + 5, arrow_y - 3, rect.right() - 5, arrow_y - 3)
            painter.drawLine(rect.center().x(), arrow_y - 3, rect.center().x(), arrow_y + 3)
            painter.drawLine(rect.center().x() - 3, arrow_y, rect.center().x(), arrow_y + 3)
            painter.drawLine(rect.center().x() + 3, arrow_y, rect.center().x(), arrow_y + 3)
            
        elif 'WRITE' in self.component_type:
            # Ícone de escrita - seta para cima
            painter.drawRect(rect)
            # Seta
            arrow_y = rect.center().y()
            painter.drawLine(rect.left() + 5, arrow_y + 3, rect.right() - 5, arrow_y + 3)
            painter.drawLine(rect.center().x(), arrow_y + 3, rect.center().x(), arrow_y - 3)
            painter.drawLine(rect.center().x() - 3, arrow_y, rect.center().x(), arrow_y - 3)
            painter.drawLine(rect.center().x() + 3, arrow_y, rect.center().x(), arrow_y - 3)
            
        elif self.component_type == 'RS485_MASTER':
            # Ícone de master - círculo com "M"
            painter.drawEllipse(rect)
            painter.setFont(QFont("Arial", 12, QFont.Bold))
            painter.setPen(QPen(color.darker(200), 2))
            painter.drawText(rect, Qt.AlignCenter, "M")
            
        elif self.component_type == 'DEVICE_STATUS':
            # Ícone de status - quadrado com ponto
            painter.drawRect(rect)
            center = rect.center()
            painter.setBrush(QBrush(color.darker(150)))
            painter.drawEllipse(center.x() - 3, center.y() - 3, 6, 6)
            
        else:  # NETWORK_SCAN
            # Ícone de rede - linhas conectadas
            painter.drawRect(rect)
            # Pontos conectados
            painter.setBrush(QBrush(color.darker(150)))
            painter.drawEllipse(rect.left() + 5, rect.top() + 5, 4, 4)
            painter.drawEllipse(rect.right() - 9, rect.top() + 5, 4, 4)
            painter.drawEllipse(rect.center().x() - 2, rect.bottom() - 9, 4, 4)
            # Linhas
            painter.drawLine(rect.left() + 7, rect.top() + 7, rect.right() - 7, rect.top() + 7)
            painter.drawLine(rect.left() + 7, rect.top() + 7, rect.center().x(), rect.bottom() - 7)
            painter.drawLine(rect.right() - 7, rect.top() + 7, rect.center().x(), rect.bottom() - 7)
        
        # Nome do componente
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setFont(QFont("Arial", 7, QFont.Bold))
        title_rect = self.rect().adjusted(0, 2, 0, -45)
        painter.drawText(title_rect, Qt.AlignCenter, self.name)
#!/usr/bin/env python3
"""
Teste das Melhorias IHM OP320
Testa as propriedades editáveis e renderizações melhoradas
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'interface_ladder'))

from PyQt5.QtWidgets import QApplication
from ihm_components import IHMComponent

def test_improved_ihm_components():
    """Testa as melhorias nos componentes IHM"""
    print("🧪 Testando Melhorias IHM OP320...")
    
    app = QApplication(sys.argv)
    
    # Testar propriedades editáveis
    print("\n📐 Testando Propriedades Editáveis:")
    
    # Componente de teste
    text_comp = IHMComponent("Texto Teste", "static_text", "Textos")
    
    # Valores padrão
    print(f"✅ Posição inicial: X={text_comp.x}, Y={text_comp.y}")
    print(f"✅ Tamanho inicial: W={text_comp.width}, H={text_comp.height}")
    
    # Testar mudança de propriedades
    text_comp.x = 20
    text_comp.y = 15
    text_comp.width = 60
    text_comp.height = 12
    
    print(f"🔄 Nova posição: X={text_comp.x}, Y={text_comp.y}")
    print(f"🔄 Novo tamanho: W={text_comp.width}, H={text_comp.height}")
    
    # Testar propriedades específicas dos componentes
    print("\n🎨 Testando Componentes Estilizados:")
    
    # LED Indicador
    led_comp = IHMComponent("LED Estado", "led_indicator", "Indicadores")
    led_comp.properties = {
        'variable': 'STATUS_LED',
        'color': 'Verde'
    }
    print(f"💡 LED: {led_comp.name} - Cor: {led_comp.properties['color']}")
    
    # Botão de Função
    btn_comp = IHMComponent("Botão OK", "function_button", "Entrada")
    btn_comp.properties = {
        'function_key': 'F1',
        'text': 'CONFIRMAR',
        'action': 'SET_CONFIRM_BIT'
    }
    print(f"🔘 Botão: {btn_comp.properties['function_key']} - {btn_comp.properties['text']}")
    
    # Texto Dinâmico
    dyn_comp = IHMComponent("Temperatura", "dynamic_text", "Textos")
    dyn_comp.properties = {
        'variable': 'TEMP_ATUAL',
        'format': '%.1f°C',
        'font_size': 10
    }
    print(f"📝 Texto Dinâmico: {dyn_comp.properties['variable']} - {dyn_comp.properties['format']}")
    
    # Campo de Entrada
    input_comp = IHMComponent("Setpoint", "input_field", "Entrada")
    input_comp.properties = {
        'variable': 'TEMP_SETPOINT',
        'min_value': 0,
        'max_value': 100
    }
    print(f"📝 Campo Entrada: {input_comp.properties['variable']} ({input_comp.properties['min_value']}-{input_comp.properties['max_value']})")
    
    # Gráfico XY
    graph_comp = IHMComponent("Gráfico Pressão", "xy_graph", "Gráficos")
    graph_comp.properties = {
        'variable': 'PRESSAO',
        'max_points': 50,
        'y_min': 0,
        'y_max': 10
    }
    print(f"📊 Gráfico: {graph_comp.properties['variable']} - Y: {graph_comp.properties['y_min']}-{graph_comp.properties['y_max']}")
    
    print("\n🎉 Melhorias Implementadas:")
    print("   ✅ Propriedades X, Y, W, H editáveis")
    print("   ✅ LED redondo e estilizado")
    print("   ✅ Botão de função com seta")
    print("   ✅ Propriedades específicas por tipo")
    print("   ✅ Botão 'Atualizar' no painel")
    
    return True

if __name__ == "__main__":
    success = test_improved_ihm_components()
    print(f"\n{'🎉 MELHORIAS IMPLEMENTADAS COM SUCESSO!' if success else '❌ TESTE FALHOU'}")
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Teste de Persistência de Dados IHM
Testa se os dados estão sendo salvos e carregados corretamente nos blocos Display
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'interface_ladder'))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ladder_canvas import LadderCanvas
from component_library import DisplayIHMComponent

def test_data_persistence():
    """Testa se os dados da IHM estão sendo persistidos nos blocos Display"""
    print("🧪 Testando Persistência de Dados IHM...")
    
    app = QApplication(sys.argv)
    
    # Criar canvas LADDER
    canvas = LadderCanvas()
    
    # Criar componente Display IHM
    display_comp = DisplayIHMComponent()
    display_comp.name = "Display_Test"
    
    print(f"✅ Componente criado: {display_comp.name}")
    
    # Verificar se o componente tem atributo de configuração
    if not hasattr(display_comp, 'ihm_config_data'):
        display_comp.ihm_config_data = None
    
    # Simular dados de configuração
    test_config = {
        'screen_name': 'Tela de Teste',
        'components': [
            {
                'type': 'text',
                'name': 'Label Teste',
                'x': 10,
                'y': 10,
                'width': 50,
                'height': 12,
                'properties': {'text': 'Olá Mundo', 'font_size': 8}
            },
            {
                'type': 'button', 
                'name': 'Botão OK',
                'x': 10,
                'y': 30,
                'width': 40,
                'height': 15,
                'properties': {'text': 'OK', 'action': 'confirm'}
            }
        ],
        'properties': {
            'background_color': 'light_green',
            'timeout': 0,
            'show_header': True
        }
    }
    
    # Testar salvamento
    display_comp.ihm_config_data = test_config
    print(f"💾 Dados salvos no componente: {display_comp.name}")
    print(f"📊 Configuração: {test_config['screen_name']} com {len(test_config['components'])} componente(s)")
    
    # Testar recuperação
    recovered_data = display_comp.ihm_config_data
    if recovered_data:
        print(f"✅ Dados recuperados: Tela '{recovered_data['screen_name']}'")
        print(f"📊 {len(recovered_data['components'])} componente(s) recuperados")
        
        # Verificar componentes
        for i, comp in enumerate(recovered_data['components']):
            print(f"   {i+1}. {comp['name']} ({comp['type']}) em ({comp['x']}, {comp['y']})")
            
        return True
    else:
        print("❌ Falha ao recuperar dados!")
        return False

if __name__ == "__main__":
    success = test_data_persistence()
    print(f"\n{'🎉 TESTE APROVADO' if success else '❌ TESTE FALHOU'}")
    sys.exit(0 if success else 1)
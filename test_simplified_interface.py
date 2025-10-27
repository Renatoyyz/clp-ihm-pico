#!/usr/bin/env python3
"""
Teste da Interface IHM Simplificada
Testa se a nova interface simplificada está funcionando corretamente
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'interface_ladder'))

from PyQt5.QtWidgets import QApplication
from ihm_config_dialog import IHMConfigDialog

def test_simplified_interface():
    """Testa a interface simplificada"""
    print("🧪 Testando Interface IHM Simplificada...")
    
    app = QApplication(sys.argv)
    
    # Criar dialog
    dialog = IHMConfigDialog()
    
    # Verificar se os elementos essenciais existem
    assert hasattr(dialog, 'screen_name_field'), "❌ Campo nome da tela não encontrado"
    assert hasattr(dialog, 'screen_info'), "❌ Info da tela não encontrada"
    assert hasattr(dialog, 'ihm_canvas'), "❌ Canvas IHM não encontrado"
    assert hasattr(dialog, 'ihm_library'), "❌ Biblioteca IHM não encontrada"
    assert hasattr(dialog, 'properties_panel'), "❌ Painel propriedades não encontrado"
    
    print("✅ Elementos da interface encontrados")
    
    # Testar métodos essenciais
    try:
        dialog.update_screen_info()
        print("✅ update_screen_info() funcionando")
    except Exception as e:
        print(f"❌ Erro em update_screen_info(): {e}")
        return False
    
    try:
        screen_data = dialog.get_screen_data()
        print(f"✅ get_screen_data() retornou: {screen_data['name']}")
    except Exception as e:
        print(f"❌ Erro em get_screen_data(): {e}")
        return False
    
    # Testar adição de componente
    try:
        dialog.add_component_to_canvas('text', 'Texto Teste')
        print("✅ Adição de componente funcionando")
    except Exception as e:
        print(f"❌ Erro ao adicionar componente: {e}")
        return False
    
    print("🎉 Teste da interface simplificada concluído com SUCESSO!")
    return True

if __name__ == "__main__":
    success = test_simplified_interface()
    sys.exit(0 if success else 1)
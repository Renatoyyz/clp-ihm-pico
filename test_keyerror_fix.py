#!/usr/bin/env python3
"""
Teste correção do KeyError
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'interface_ladder'))

try:
    from PyQt5.QtWidgets import QApplication
    from interface_ladder.ihm_config_dialog import IHMConfigDialog
    from interface_ladder.ihm_components import IHMComponent
    
    print("✅ Teste Correção KeyError")
    print("="*40)
    
    app = QApplication(sys.argv)
    
    # Testar criação de componente e get_display_data
    component = IHMComponent("Teste", "text", "display")
    display_data = component.get_display_data()
    
    print("📊 Dados do componente:")
    for key, value in display_data.items():
        print(f"  {key}: {value}")
    
    # Verificar se tem todas as chaves necessárias
    required_keys = ['type', 'name', 'x', 'y', 'width', 'height', 'properties']
    missing_keys = [key for key in required_keys if key not in display_data]
    
    if missing_keys:
        print(f"❌ Chaves faltando: {missing_keys}")
    else:
        print("✅ Todas as chaves necessárias estão presentes")
    
    # Testar criação da dialog
    try:
        dialog = IHMConfigDialog()
        print("✅ Dialog criada sem erro")
        
        # Testar se há telas padrão
        if hasattr(dialog, 'screen_manager') and dialog.screen_manager.screens:
            screen = dialog.screen_manager.screens[0]
            print(f"✅ Tela padrão: '{screen.name}' com {len(screen.components)} componentes")
        
    except Exception as e:
        print(f"❌ Erro ao criar dialog: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Teste concluído!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
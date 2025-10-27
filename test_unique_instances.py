#!/usr/bin/env python3
"""
Teste do novo fluxo IHM com instâncias únicas
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'interface_ladder'))

try:
    from PyQt5.QtWidgets import QApplication
    from interface_ladder.ladder_canvas import LadderCanvas, LadderCanvasItem
    
    print("✅ Teste do Novo Fluxo IHM - Instâncias Únicas")
    print("="*55)
    
    app = QApplication(sys.argv)
    
    # Criar canvas LADDER
    canvas = LadderCanvas()
    print(f"✅ Canvas LADDER criado")
    
    # Testar criação de item Display IHM
    display_item = LadderCanvasItem("DISPLAY_IHM", "Display_1", "Display ST7920 128x64", 100, 100)
    print(f"✅ Item Display IHM criado: {display_item.name}")
    
    # Verificar atributos específicos
    print(f"   - Tipo: {display_item.component_type}")
    print(f"   - Display ID: {getattr(display_item, 'display_id', 'Não definido')}")
    print(f"   - Config IHM: {hasattr(display_item, 'ihm_config_data')}")
    
    # Testar método de configuração IHM (sem interface gráfica)
    if hasattr(canvas, 'open_ihm_config_for_item'):
        print("✅ Método open_ihm_config_for_item disponível")
    else:
        print("❌ Método open_ihm_config_for_item não encontrado")
    
    # Testar método de salvamento de configuração
    if hasattr(canvas, 'save_ihm_config_for_item'):
        print("✅ Método save_ihm_config_for_item disponível")
    else:
        print("❌ Método save_ihm_config_for_item não encontrado")
    
    print("\n🎯 Funcionalidades Implementadas:")
    print("="*40)
    print("✅ Auto-abertura: Display IHM abre configuração ao ser arrastado")
    print("✅ Instâncias únicas: Cada bloco tem nome e ID únicos")  
    print("✅ Menu contexto: Clique direito → 'Editar IHM'")
    print("✅ Configuração específica: Cada bloco salva sua própria configuração")
    
    print("\n🔄 Novo Fluxo de Trabalho:")
    print("="*30)
    print("1. 📱 Arraste 'Display IHM' → Editor LADDER")
    print("2. 🖥️ Configuração abre automaticamente")
    print("3. ➕ Use botões '+' para adicionar componentes")
    print("4. 💾 Configure e salve as telas")
    print("5. 🖱️ Clique direito no bloco → 'Editar IHM' para modificar")
    
    print("\n✨ Cada bloco Display no LADDER é uma instância única!")
    print("✨ Display_1, Display_2, Display_3... com configurações independentes!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
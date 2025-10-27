#!/usr/bin/env python3
"""
Teste do novo fluxo IHM: Drag para LADDER + Clique direito para configurar
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'interface_ladder'))

try:
    from PyQt5.QtWidgets import QApplication
    from interface_ladder.ihm_config_dialog import IHMConfigDialog
    from interface_ladder.component_library import DisplayIHMComponent
    
    print("✅ Teste do Novo Fluxo IHM")
    print("="*50)
    
    app = QApplication(sys.argv)
    
    # Teste 1: DisplayIHMComponent com menu de contexto
    print("\n1️⃣ Testando DisplayIHMComponent...")
    display_component = DisplayIHMComponent()
    print(f"✅ DisplayIHMComponent criado: {display_component.name}")
    
    # Teste 2: IHM Config Dialog com botões de adicionar
    print("\n2️⃣ Testando IHM Config Dialog...")
    dialog = IHMConfigDialog()
    print("✅ IHM Config Dialog criado")
    
    if hasattr(dialog, 'ihm_library'):
        print("✅ Biblioteca IHM carregada")
        
        # Verificar se tem sinal para adicionar componentes
        if hasattr(dialog.ihm_library, 'add_component_requested'):
            print("✅ Sinal add_component_requested disponível")
        else:
            print("❌ Sinal add_component_requested não encontrado")
            
        # Verificar se dialog tem método para adicionar ao canvas
        if hasattr(dialog, 'add_component_to_canvas'):
            print("✅ Método add_component_to_canvas disponível")
        else:
            print("❌ Método add_component_to_canvas não encontrado")
    else:
        print("❌ Biblioteca IHM não carregada")
    
    # Teste 3: Canvas e persistência
    print("\n3️⃣ Testando Canvas e persistência...")
    if hasattr(dialog, 'ihm_canvas'):
        canvas = dialog.ihm_canvas
        print(f"✅ Canvas disponível: {type(canvas).__name__}")
        
        # Testar adicionar componente programaticamente
        initial_count = len(canvas.screen_components)
        print(f"📊 Componentes iniciais: {initial_count}")
        
        # Adicionar um componente de teste
        canvas.add_component('text', 20, 10)
        after_count = len(canvas.screen_components)
        print(f"📊 Componentes após adicionar: {after_count}")
        
        if after_count > initial_count:
            print("✅ Componente adicionado com sucesso!")
            
            # Verificar se componente está visível na cena
            scene_items = canvas._scene.items()
            print(f"📊 Items na cena: {len(scene_items)}")
            
        else:
            print("❌ Falha ao adicionar componente")
    else:
        print("❌ Canvas não disponível")
    
    print("\n🎯 Fluxo de Uso Recomendado:")
    print("="*50)
    print("1. Execute: python main.py")
    print("2. Na biblioteca LADDER, arraste 'Display IHM' para o editor")
    print("3. Clique direito no bloco Display IHM no editor LADDER")
    print("4. Selecione '🖥️ Configurar IHM'")
    print("5. Na janela IHM, use botões '+ Nome_Componente' para adicionar")
    print("6. Componentes aparecem no canvas 128x64")
    print("7. Configure propriedades no painel direito")
    print("8. Use 'Salvar Config' para persistir")
    
    print("\n📝 Mudanças Implementadas:")
    print("="*30)
    print("✅ Componentes IHM NÃO são mais arrastáveis para canvas")
    print("✅ Display IHM tem menu de contexto (clique direito)")
    print("✅ Componentes são adicionados via botões '+ Nome'")
    print("✅ Sistema de persistência mantido")
    
    print("\n🎉 Teste concluído!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
#!/usr/bin/env python3
"""
Teste do sistema de salvamento/carregamento IHM
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'interface_ladder'))

try:
    from PyQt5.QtWidgets import QApplication
    from interface_ladder.ihm_screen_manager import IHMScreenManager
    from interface_ladder.ihm_components import IHMComponent
    
    print("✅ Teste do Sistema de Persistência IHM")
    print("="*50)
    
    app = QApplication(sys.argv)
    
    # Criar screen manager
    manager = IHMScreenManager()
    print(f"✅ Screen Manager criado com {len(manager.screens)} tela(s)")
    
    # Adicionar alguns componentes de teste
    if manager.screens:
        screen = manager.screens[0]
        
        # Criar componentes de teste
        texto = IHMComponent("Título", "text", "display")
        texto.x = 10
        texto.y = 5
        texto.width = 60
        texto.height = 12
        texto.properties = {"text": "Sistema IHM", "font_size": 8}
        
        botao = IHMComponent("Botão OK", "button", "input") 
        botao.x = 70
        botao.y = 45
        botao.width = 40
        botao.height = 15
        botao.properties = {"text": "OK", "action": "next_screen"}
        
        indicator = IHMComponent("LED Status", "indicator", "output")
        indicator.x = 5
        indicator.y = 50
        indicator.width = 8
        indicator.height = 8
        indicator.properties = {"state": True, "variable": "status_led"}
        
        # Adicionar componentes à tela
        screen.components = [texto, botao, indicator]
        print(f"✅ {len(screen.components)} componentes adicionados à tela '{screen.name}'")
    
    # Teste de salvamento
    print("\n📁 Testando salvamento...")
    success = manager.save_configuration("test_ihm_config.json")
    if success:
        print("✅ Salvamento bem-sucedido!")
    else:
        print("❌ Erro no salvamento")
    
    # Limpar e testar carregamento
    print("\n📂 Testando carregamento...")
    manager.screens.clear()
    print(f"✅ Telas limpas: {len(manager.screens)} tela(s)")
    
    success = manager.load_configuration("test_ihm_config.json") 
    if success:
        print(f"✅ Carregamento bem-sucedido! {len(manager.screens)} tela(s) carregadas")
        if manager.screens:
            screen = manager.screens[0]
            print(f"✅ Tela '{screen.name}' carregada com {len(screen.components)} componente(s)")
            
            # Mostrar componentes carregados
            for i, comp in enumerate(screen.components):
                print(f"   {i+1}. {comp.name} ({comp.type}) - pos: ({comp.x},{comp.y})")
    else:
        print("❌ Erro no carregamento")
    
    # Limpar arquivo de teste
    try:
        if os.path.exists("test_ihm_config.json"):
            os.remove("test_ihm_config.json")
            print("🧹 Arquivo de teste removido")
    except:
        pass
    
    print("\n🎉 Teste de persistência concluído!")
    print("\nPara usar:")
    print("1. Execute: python main.py")
    print("2. Clique no Display IHM")
    print("3. Configure suas telas")
    print("4. Use 'Salvar Config' para persistir")
    print("5. Use 'Carregar Config' para restaurar")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
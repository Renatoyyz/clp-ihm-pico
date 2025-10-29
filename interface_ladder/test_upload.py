#!/usr/bin/env python3
"""
Script de teste para upload de arquivo no Pico
"""

import sys
import os

# Adicionar path para importar módulos
sys.path.insert(0, os.path.dirname(__file__))

from pico_connection_manager import pico_manager

def test_upload():
    """Testa upload de arquivo"""
    
    print("="*60)
    print("TESTE DE UPLOAD PARA RASPBERRY PI PICO")
    print("="*60)
    
    # 1. Verificar conexão
    print("\n1. Verificando conexão...")
    status = pico_manager.get_status_dict()
    print(f"   Conectado: {status['connected']}")
    print(f"   Porta: {status['port']}")
    print(f"   Serial disponível: {status['available']}")
    
    if not status['connected']:
        print("\n❌ Pico não está conectado!")
        print("   Execute primeiro: python app.py")
        print("   E conecte ao Pico através do menu")
        return
    
    # 2. Criar arquivo de teste
    print("\n2. Criando arquivo de teste...")
    test_file = "/tmp/test_upload.py"
    test_content = """# Arquivo de teste
print('Hello from Pico!')
print('Upload funcionou!')

import sys
print(f'Python: {sys.version}')
"""
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    print(f"   Arquivo criado: {test_file}")
    print(f"   Tamanho: {len(test_content)} bytes")
    
    # 3. Fazer upload
    print("\n3. Iniciando upload...")
    success, message = pico_manager.upload_file(test_file, "test_upload.py")
    
    print(f"\n   Resultado: {'✅ SUCESSO' if success else '❌ FALHA'}")
    print(f"   Mensagem: {message}")
    
    # 4. Verificar arquivo no Pico
    if success:
        print("\n4. Verificando arquivo no Pico...")
        success, response = pico_manager.send_command("import os; print(os.listdir())")
        if success:
            print(f"   Arquivos no Pico: {response}")
            
            # Tentar executar arquivo
            print("\n5. Executando arquivo de teste...")
            success, response = pico_manager.send_command("exec(open('test_upload.py').read())")
            if success:
                print(f"   Saída:\n{response}")
    
    # 6. Teste com main_.py
    print("\n" + "="*60)
    print("6. Testando upload de main_.py...")
    print("="*60)
    
    main_file = "../generated_code/main_.py"
    if os.path.exists(main_file):
        print(f"\n   Arquivo encontrado: {main_file}")
        file_size = os.path.getsize(main_file)
        print(f"   Tamanho: {file_size} bytes")
        
        # Upload
        print("\n   Fazendo upload como main.py...")
        success, message = pico_manager.upload_file(main_file, "main.py")
        
        print(f"\n   Resultado: {'✅ SUCESSO' if success else '❌ FALHA'}")
        print(f"   Mensagem: {message}")
        
        if success:
            print("\n   ✅ main.py enviado para o Pico!")
            print("   💡 Execute soft reset para rodar: Ctrl+D no REPL")
    else:
        print(f"\n   ⚠️ Arquivo não encontrado: {main_file}")
        print("   Execute 'Exportar → Python' primeiro")
    
    print("\n" + "="*60)
    print("TESTE CONCLUÍDO")
    print("="*60)

if __name__ == "__main__":
    test_upload()

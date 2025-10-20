#!/bin/bash
# setup_venv.sh - Script para configurar ambiente virtual
# Funciona com diferentes instalações de Python no macOS

echo "🥧 Raspberry Pi Pico Uploader - Setup do Ambiente Virtual"
echo "========================================================="

# Função para testar pip/SSL
test_pip_ssl() {
    python3 -c "import ssl; import pip" 2>/dev/null
    return $?
}

# Função para instalar dependências via pip
install_with_pip() {
    echo "📦 Tentando instalação via pip..."
    pip install pyserial PyQt5
    return $?
}

# Função para baixar e instalar manualmente
install_manual() {
    echo "📥 Instalação manual das dependências..."
    
    # Criar diretório para downloads
    mkdir -p manual_packages
    cd manual_packages
    
    echo "⬇️  Baixando pyserial..."
    curl -L -o pyserial.tar.gz https://files.pythonhosted.org/packages/1e/7d/ae3f0a63f41e4d2f6cb66a5b57197850f919f59e558159a4dd3a818f5082/pyserial-3.5.tar.gz
    
    if [ $? -eq 0 ]; then
        echo "📦 Instalando pyserial manualmente..."
        tar -xzf pyserial.tar.gz
        cd pyserial-3.5
        python setup.py install
        cd ..
    fi
    
    cd ..
    echo "✅ Tentativa de instalação manual concluída"
}

# Verificar se já existe ambiente virtual
if [ -d ".venv" ]; then
    echo "✅ Ambiente virtual já existe"
    source .venv/bin/activate
else
    echo "🔧 Criando ambiente virtual..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

echo "🔍 Verificando ambiente..."
echo "Python: $(which python)"
echo "Pip: $(which pip)"

# Tentar diferentes métodos de instalação
if test_pip_ssl; then
    echo "✅ SSL/TLS funcionando, tentando pip normal..."
    if install_with_pip; then
        echo "✅ Dependências instaladas via pip!"
    else
        echo "❌ Falha no pip, tentando instalação manual..."
        install_manual
    fi
else
    echo "⚠️  Problema com SSL/TLS, pulando instalação de dependências"
    echo "🔧 Você pode usar a versão terminal que funciona sem dependências"
fi

# Testar se pyserial funciona
python -c "import serial; print('✅ pyserial funcionando!')" 2>/dev/null || echo "⚠️  pyserial não disponível"

echo ""
echo "========================================================="
echo "🎯 AMBIENTE VIRTUAL CONFIGURADO!"
echo "========================================================="
echo "Para ativar:"
echo "  source .venv/bin/activate"
echo ""
echo "Para executar:"
echo "  python terminal_uploader.py    # Sempre funciona"
echo "  python simple_pico_uploader.py # Requer PyQt5"
echo ""
echo "Para desativar:"
echo "  deactivate"
echo "========================================================="
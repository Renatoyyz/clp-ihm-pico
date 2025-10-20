#!/bin/bash
# Script de instalação para o Pico Uploader
# Funciona em macOS, Linux e Windows (via Git Bash)

echo "=== Raspberry Pi Pico File Uploader - Setup ==="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Instale o Python 3 primeiro."
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"

# Verifica se pip está disponível
if ! command -v pip3 &> /dev/null; then
    echo "Erro: pip3 não encontrado. Instale o pip primeiro."
    exit 1
fi

echo "✓ pip3 encontrado"

# Instala dependências
echo ""
echo "Instalando dependências Python..."
echo "Isso pode levar alguns minutos..."

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependências instaladas com sucesso!"
else
    echo "✗ Erro na instalação das dependências"
    echo "Tente instalar manualmente:"
    echo "  pip3 install pyserial PyQt5"
    exit 1
fi

# Testa a instalação
echo ""
echo "Testando instalação..."

python3 -c "import serial; import PyQt5; print('✓ Todas as bibliotecas importadas com sucesso!')"

if [ $? -eq 0 ]; then
    echo ""
    echo "=== INSTALAÇÃO CONCLUÍDA COM SUCESSO! ==="
    echo ""
    echo "Para executar a aplicação:"
    echo "  python3 simple_pico_uploader.py"
    echo ""
    echo "Ou a versão completa:"
    echo "  python3 pico_uploader.py"
    echo ""
    echo "Certifique-se de que o Raspberry Pi Pico esteja:"
    echo "1. Conectado via USB"
    echo "2. Com MicroPython instalado"
    echo "3. Aparecendo como porta serial no sistema"
else
    echo "✗ Erro no teste da instalação"
fi
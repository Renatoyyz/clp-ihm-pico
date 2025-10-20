#!/bin/bash
# activate.sh - Ativa ambiente virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Ambiente virtual ativado"
    echo "Para desativar: deactivate"
else
    echo "❌ Ambiente virtual não encontrado"
    echo "Execute: python3 -m venv .venv"
fi

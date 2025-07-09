#!/bin/bash

echo "=== Bot Discord - Street Car Club Whitelist ==="
echo "Iniciando bot do Street Car Club..."
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python3 primeiro."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale o pip3 primeiro."
    exit 1
fi

echo "✅ Verificando dependências..."
pip3 install -r requirements.txt

echo
echo "🚀 Iniciando bot..."
python3 bot.py 
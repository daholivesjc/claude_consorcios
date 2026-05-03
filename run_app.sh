#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Instalando dependências..."
pip install -q -r requirements.txt

echo "Iniciando ClaudeConsórcios..."
streamlit run app.py --server.port 8502 --server.headless false

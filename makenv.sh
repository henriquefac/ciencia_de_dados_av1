#!/bin/bash

echo "Iniciando projeto"

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual"
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
fi

# Ativa o ambiente virtual
source start.sh


if ! python -c "import requests" &> /dev/null; then
    echo "Erro: requests não encontrado. Instalando..."
    pip install requests
fi

# Executa os scripts
python src/webscraping/utils_web/getlinks.py
python src/webscraping/utils_web/download_files.py

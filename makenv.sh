#!/bin/bash

echo "Iniciando projeto"

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual"
    python3 -m venv .venv

    # Define as variáveis de ambiente para o ambiente virtual
    echo "export PYTHONPATH=$(pwd)" >> .venv/bin/activate
    echo "export JUPYTER_PATH=$(pwd)" >> .venv/bin/activate

    # Ativa o ambiente virtual
    source .venv/bin/activate
    
    # Atualiza o pip e instala dependências
    python3 -m pip install --upgrade pip

    # Verifica se requirements.txt existe antes de instalar
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "Aviso: requirements.txt não encontrado. Nenhum pacote foi instalado."
    fi

    # criar kernel
    python -m ipykernel install --user --name=ciencia_de_dados_av1 --display-name "Python (ciencia_de_dados_av1)"

    deactivate
fi

# Ativa o ambiente virtual
source .venv/bin/activate

# Verifica se 'requests' está instalado corretamente
if ! python -c "import requests" &> /dev/null; then
    echo "Erro: requests não encontrado. Instalando..."
    pip install requests
fi

# Executa os scripts
python src/webscraping/utils_web/getlinks.py
python src/webscraping/utils_web/download_files.py

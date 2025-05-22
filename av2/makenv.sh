#!/bin/bash

echo "Iniciando projeto"

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual"
    py -3 -m venv .venv # MODIFICADO AQUI

    # Define as variáveis de ambiente para o ambiente virtual
    # Nota: A forma como você está adicionando ao activate pode não ser ideal
    # para todas as shells, mas vamos manter por enquanto.
    echo "export PYTHONPATH=$(pwd)" >> .venv/bin/activate
    echo "export JUPYTER_PATH=$(pwd)" >> .venv/bin/activate

    # Ativa o ambiente virtual
    source .venv/bin/activate
    
    # Atualiza o pip e instala dependências
    py -3 -m pip install --upgrade pip # MODIFICADO AQUI

    # Verifica se requirements.txt existe antes de instalar
    if [ -f "requirements.txt" ]; then
        py -3 -m pip install -r requirements.txt # MODIFICADO AQUI
    else
        echo "Aviso: requirements.txt não encontrado. Nenhum pacote foi instalado."
    fi

    # criar kernel (Esta linha parece incompleta, mas o deactivate está correto)
    deactivate
fi

# Ativa o ambiente virtual
source .venv/bin/activate

# Verifica se 'requests' está instalado corretamente
# Usaremos 'py -3' para consistência, embora 'py' provavelmente funcione
if ! py -3 -c "import requests" &> /dev/null; then # MODIFICADO AQUI
    echo "Erro: requests não encontrado. Instalando..."
    py -3 -m pip install requests # MODIFICADO AQUI
fi

# Executa os scripts
py -3 src/webscraping/utils_web/getlinks.py # MODIFICADO AQUI
py -3 src/webscraping/utils_web/download_files.py # MODIFICADO AQUI

echo "Script finalizado." # Adicionado para feedback
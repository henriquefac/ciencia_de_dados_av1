echo "Iniciando projeto"
if [ ! ".env"]; then
    echo "Criando ambiente virtual"
    python3 -m venv .env
    source env/bin/activate
    pip -r requirements.txt
    deactivate
fi

source start.sh
python src/webscraping/utils_web/getlinks.py
python src/webscraping/utils_web/download_files.py
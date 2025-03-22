import requests
from bs4 import BeautifulSoup
import os
from config import *

# aqui vai ser usado para colectar os links de download

LINK_DIR = Config.get_path_links()

# primeiro, é preciso pegar o link da página principal
def get_links_web():
    LINK_PAGE_PATH = LINK_DIR["page"]

    link = open(LINK_PAGE_PATH, "r").readline().strip()

    requsicao = requests.get(link)

    site = BeautifulSoup(requsicao.text, "html.parser")

    content_selection = site.find("div", id="parent-fieldname-text")

    list_links = list(map(lambda x: x["href"],content_selection.find_all(name="a")))

    # armazenar links
    return list_links

def get_links_files():
    LINK_DOWNLOAD_PATH = LINK_DIR["links-download"]
    
    with open(LINK_DOWNLOAD_PATH, "r", encoding="utf-8") as file:
        links = [linha.strip() for linha in file if linha.strip()]
    
    return links

def download_from_links(list_links):
    # Caminho para salvar os links coletados
    LINK_DOWNLOAD_PATH = LINK_DIR["links-download"]

    if not LINK_DOWNLOAD_PATH:
        raise FileNotFoundError("Arquivo 'links-download.txt' não encontrado em links-download/")

    # Salva os links no arquivo
    with open(LINK_DOWNLOAD_PATH, "w", encoding="utf-8") as file:
        for link in list_links:
            file.write(link + "\n")

    print(f"{len(list_links)} links salvos em {LINK_DOWNLOAD_PATH}")
    
    
if __name__ == "__main__":
    list_links = get_links_web()
    download_from_links(list_links)
    for link in (get_links_files()):
        print(link)
    
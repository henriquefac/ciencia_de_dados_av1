from getlinks import get_links_files
from config import *

import time
import requests
import zipfile
from pathlib import Path



URL_LIST = get_links_files()

# download das url de download

# criar diretórios para carregar os dados a partir da url de download

def create_dir_download(url: str):
    name = url.split("/")[-1][:-4]
    dir_path = Config.DATA_PATH / name
        
    return dir_path

def download_from_url(url: str, chunk_size: int = 1024 * 1024, tentativas:int = 3, espera: int = 5):

    dir_path = create_dir_download(url)
    print(dir_path)
    zip_name = url.split("/")[-1]
    zip_path = dir_path / zip_name
    
    # path para armazenar os dados
    if zip_path.exists():
        print("Já foi baixado")
        return zip_path

    dir_path.mkdir(parents=True, exist_ok=True)

    for tentativa in range(tentativas):
        try:
            resposta = requests.get(url,  headers={"User-Agent": "Mozilla/5.0"}, stream=True)
            resposta.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {tentativa+1} falhou: {e}")
            time.sleep(espera)
    else:
        raise Exception("Falha ao baixar após tentativas")
            
    tamanho_total = int(resposta.headers.get('content-length', 0))
    baixado = 0
    
   
    with open(zip_path, "wb") as f:
        for chunk in resposta.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                baixado += len(chunk)
                print(f"Baixado: {baixado / (1024*1024):.2f} MB de {tamanho_total / (1024*1024):.2f} MB", end="\r")
    return zip_path
    

def extract_zip_by_path(zip_path: Path):
    base_dir = zip_path.parent
    destino = base_dir / Path(zip_path.stem + "_extract")
    
    if destino.exists():
        print("Já foi extraído")
        return
    # crir diretório onde os dados vão ser extraídos
    destino.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destino)

if __name__ == "__main__":
    print(extract_zip_by_path(download_from_url(URL_LIST[0])))
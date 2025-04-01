from config import Config
import pandas as pd
from pathlib import Path
from utils import Dicionario
# recebe camiho para um arquivo xlsx e transforma num csv
# funções para isso
# função específica para DICIONÁRIO

# a partir de um caminho para um arquiv, crair um diretódio com onome do arquivo no mesmo nível
def make_dir(path: Path):
    name = path.stem
    root = path.parent
    dir_path = root / f"{name}_csv"
    
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def file_path_csv(name: str, path_dir: Path):
    return path_dir / f"{name}.csv"
# função para transformar o DICIONARIo xlsx em um csv

def dict_xlsx_csv(path_xlsx: Path):
    # criar xl_file
    xl_file = pd.ExcelFile(path_xlsx)

    # diretório para os arquivos csv
    dir_path = make_dir(path_xlsx)

    dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}
    
    for name, df in dfs.items():
        df.to_csv(file_path_csv(name, dir_path), index=False)



if __name__ == "__main__":
    data_dirs = Config.get_path_dir_data()
    path_xlsx = data_dirs["microdados_enem_2023_extract"]["Dicionário_Microdados_Enem_2023.xlsx"]
    dict_xlsx_csv(path_xlsx)
    path_csv = data_dirs["microdados_enem_2023_extract"]["MICRODADOS_ENEM_2023.csv"]
    dict_ = Dicionario(path_csv)
    print(dict_.tabel)

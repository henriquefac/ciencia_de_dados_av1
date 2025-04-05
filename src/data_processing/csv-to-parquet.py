from config import Config
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import pyarrow as pa


def make_dir(path: Path):
    name = path.stem
    root = path.parent
    dir_path = root / f"{name}_parquet"
    
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def file_path_parquet(path_dir: Path, part: int):
    return path_dir / f"part_{part}.parquet"

def csv_to_parquet(path_csv: Path, chunk_size=500_000):
    # Criar diretório para os arquivos Parquet
    dir_path = make_dir(path_csv)
    
    part_path = []
    
    # Ler CSV em chunks e salvar cada um como Parquet
    for i, chunk in enumerate(pd.read_csv(path_csv, chunksize=chunk_size, low_memory=False, encoding="latin1", sep=";")):
        parquet_path = file_path_parquet(dir_path, i)
        chunk.to_parquet(parquet_path, engine="pyarrow", index=False)
        part_path.append(parquet_path)
        print(f"Parte {i} salva em {parquet_path}")
    
    return part_path

def merge_parquet_files(part_paths, output_path):
    """ Junta arquivos Parquet em um único arquivo final. """
    first = True  # Flag para saber quando é o primeiro arquivo

    for part in part_paths:
        df = pd.read_parquet(part)
        
        if first:
            # Se for o primeiro arquivo, cria o Parquet
            df.to_parquet(output_path, engine="pyarrow", index=False)
            first = False
        else:
            # Caso contrário, usa pyarrow para anexar ao Parquet existente
            table = pq.read_table(part)  # Lê o arquivo Parquet
            existing_table = pq.read_table(output_path)  # Lê o arquivo Parquet existente
            new_table = pa.concat_tables([existing_table, table])  # Concatena as tabelas
            pq.write_table(new_table, output_path)  # Escreve a tabela concatenada

    print(f"Arquivo Parquet final salvo em: {output_path}")
if __name__ == "__main__":
    data_dirs = Config.get_path_dir_data()
    path_csv = data_dirs["DADOS"]["MICRODADOS_ENEM_2023.csv"]
    
    part_paths = list(data_dirs["DADOS"]["MICRODADOS_ENEM_2023_parquet"].list_file().values())
    
    final_parquet_path = path_csv.with_suffix(".parquet")
    
    merge_parquet_files(part_paths, final_parquet_path)
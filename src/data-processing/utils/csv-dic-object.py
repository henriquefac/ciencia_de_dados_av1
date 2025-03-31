# criar um objeto para passar compreender os dados dos participantes e suas catgorias
# vou fazer para 2023
from config import Config
from pathlib import Path
import pandas as pd
import csv

CABECALHO = ["Nome da variavel", "Descricao", "Variavel Categorica", "Tamanho", "Tipo"]

def getCleanCSV(path: Path):
    with open(path, mode="r") as file:
        csvFile = csv.reader(file)

        # Pular as 5 primeiras linhas
        for _ in range(5):
            next(csvFile, None)

        # Retornar as linhas restantes
        return list(csvFile)[: -7]


def get_category_lines(lines: list[list], variavel: str)->list[list]:
    index_first = 0
    index_last = 0
    for i, line in enumerate(lines):
        if index_first > 0 and line[0] != '':
            index_last = i
            break
        if line[0] == variavel:
            index_first = i

    cut_lines = lines[index_first:index_last]
    new_lines = [line[2:4] for line in cut_lines]
    return new_lines
    

def get_categorys(csv_path: Path, list_variavel):
    list_lines = getCleanCSV(csv_path)
    return {variavel: pd.DataFrame(get_category_lines(list_lines, variavel), columns = ["categoria", "descricao"])
             for variavel in list_variavel}



# criar tabela principal
def create_dataframe(csv_path: Path):
    list_lines = getCleanCSV(csv_path)

    # eliminar linhas cujo primeiro element seja vazio
    main_lines = [ line for line in list_lines if line[0] != '']

    # Corrigir "Variavel Categorica"
    for line in main_lines:
        line[2] = not(line[2] == '')
        line[3] = line[4]
        line[4] = line[5]
        line.pop()

    
    # Criar DataFrame usando CABECALHO fixo
    df = pd.DataFrame(main_lines, columns=CABECALHO)

    return df


if __name__ == "__main__":
    data_dict = Config.get_path_dir_data()
    csv_dict = data_dict["MICRODADOS_ENEM_2023"]
    df = create_dataframe(csv_dict)
    result = list(df.loc[df["Variavel Categorica"] == True, "Nome da variavel"])
    print(result)
    print(get_categorys(csv_dict, result)[result[0]])
# criar um objeto para passar compreender os dados dos participantes e suas catgorias
# vou fazer para 2023
from config import Config
from pathlib import Path
import pandas as pd
import csv

class ItemDict():

    CABECALHO = ["Nome da variavel", "Descricao", "Variavel Categorica", "Tamanho", "Tipo"]

    def __init__(self, path_csv: Path):
        self.path_csv = path_csv
        self.tabel = self.create_dataframe()
        self.legenda = self.get_categorys()
        
    def getCleanCSV(self):
        with open(self.path_csv, mode="r", encoding="latin1") as file:
            csvFile = csv.reader(file)

            # Pular as 5 primeiras linhas
            for _ in range(2):
                next(csvFile, None)

            # Retornar as linhas restantes
            return list(csvFile)[: -1]
    # para uma variavel categorica, pegar linhas relacionadas a ela 
    def get_category_lines(self, lines: list[list], variavel: str)->list[list]:
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

    # para cada categoria, criar um data frame de legenda das categorias de cada variavel
    def get_categorys(self):
        list_variavel = self.tabel[self.tabel["Variavel Categorica"] == True]["Nome da variavel"]
        list_lines = self.getCleanCSV()
        return {variavel: pd.DataFrame(self.get_category_lines(list_lines, variavel), columns = ["categoria", "descricao"])
                 for variavel in list_variavel}

    # criar tabela principal
    def create_dataframe(self):
        list_lines = self.getCleanCSV()

        # eliminar linhas cujo primeiro element seja vazio
        main_lines = [ line for line in list_lines if line[0] != '']

        # Corrigir "Variavel Categorica"
        try:
            for line in main_lines:
                line[2] = not(line[2] == '')
                line[3] = line[4]
                line[4] = line[5]
                line.pop()
        except IndexError as e:
            print(line)
            raise e

        # Criar DataFrame usando CABECALHO fixo
        df = pd.DataFrame(main_lines, columns=self.CABECALHO)

        return df




if __name__ == "__main__":
    data_dict = Config.get_path_dir_data()
    csv_dict = data_dict["DICIONÁRIO"]["ITENS_PROVA_2023.csv"]
    print(csv_dict)   
    dicionario = ItemDict(csv_dict)
    print(dicionario.tabel)
    for key , value in dicionario.legenda.items():
        print(key)
        print(value)
        print("----------------------------------------------------------")
from pathlib import Path
from typing import Union


# classe para gerenciar diretório e seus arquivos
class DirManager():
    def __init__(self, dir_path: Union[Path, "DirManager"]):
        self.dir_path = Path(dir_path) if isinstance(dir_path, (str, Path)) else dir_path.dir_path
    
    def list_dir(self)->dict[str, 'DirManager']:
        return {dir.name : DirManager(dir)  for dir in self.dir_path.iterdir() if dir.is_dir()}
    
    def list_file(self)->dict[str, Path]:
        return {file.name: file for file in self.dir_path.iterdir() if file.is_file()}

    def __str__(self) -> str:
        """Retorna o caminho como string ao chamar print(obj)."""
        return str(self.dir_path)

    def __repr__(self) -> str:
        """Retorna a representação do objeto no modo debug."""
        return f"DirManager({self.dir_path})"
    
    def __getitem__(self, key: str) -> 'DirManager':
        # Busca primeiro no nível atual
        dirs = self.list_dir()
        files = self.list_file()

        if key in dirs:
            return dirs[key]
        if key in files:
            return files[key]

        for sub_dir in dirs.values():
            try:
                return sub_dir[key]
            except KeyError:
                continue
        
        raise KeyError(f"'{key}' não encontrado em {self.dir_path} e subdiretórios.")

    
class Config:
    BASE_PATH = Path(__file__).resolve().parent
    FILE_DIR_PATH = BASE_PATH / "files"
    DATA_PATH = FILE_DIR_PATH / "data"
    LINKS_DIR = FILE_DIR_PATH / "links"

    @classmethod
    def get_path_links(cls) -> DirManager:
        return DirManager(cls.LINKS_DIR)
    
    @classmethod
    def get_path_dir_data(cls) -> DirManager:
        return DirManager(cls.DATA_PATH)


if __name__ == "__main__":
    # Obtendo os diretórios dentro de DATA_PATH
    data_dirs = Config.get_path_dir_data()
    data_extract = data_dirs["microdados_enem_2023"]["microdados_enem_2023_extract"]

    print(data_extract.list_dir())


from pathlib import Path
from typing import Union


# classe para gerenciar diretório e seus arquivos
class DirManager():
    def __init__(self, dir_path: Union[Path, "DirManager"]):
        self.dir_path = Path(dir_path) if isinstance(dir_path, (str, Path)) else dir_path.dir_path
    
    def list_dir(self)->dict[str, 'DirManager']:
        return {dir.name : DirManager(dir)  for dir in self.dir_path.iterdir() if dir.is_dir()}
    
    def list_file(self)->dict[str, Path]:
        return {file.stem: file for file in self.dir_path.iterdir() if file.is_file()}

    def __str__(self) -> str:
        """Retorna o caminho como string ao chamar print(obj)."""
        return str(self.dir_path)

    def __repr__(self) -> str:
        """Retorna a representação do objeto no modo debug."""
        return f"DirManager({self.dir_path})"
    
class Config:
    BASE_PATH = Path(__file__).resolve().parent
    FILE_DIR_PATH = BASE_PATH / "files"
    DATA_PATH = FILE_DIR_PATH / "data"
    LINKS_DIR = FILE_DIR_PATH / "links"

    @classmethod
    def get_path_links(cls) -> dict[str, Path]:
        return {file.stem: file for file in cls.LINKS_DIR.iterdir() if file.is_file()}
    
    @classmethod
    def get_path_dir_data(cls) -> dict[str, DirManager]:
        return {dir.name : DirManager(dir)  for dir in cls.DATA_PATH.iterdir() if dir.is_dir()}


if __name__ == "__main__":
    # Obtendo os diretórios dentro de DATA_PATH
    data_dirs = Config.get_path_dir_data()
    data_extract = data_dirs["microdados_enem_2023"]

    print(data_extract.list_dir()["microdados_enem_2023_extract"])


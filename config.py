from pathlib import Path

class Config:
    BASE_PATH = Path(__file__).resolve().parent
    FILE_DIR_PATH = BASE_PATH / "files"
    DATA_PATH = FILE_DIR_PATH / "data"
    LINKS_DIR = FILE_DIR_PATH / "links"

    @classmethod
    def get_path_links(cls) -> dict[str, Path]:
        return {file.name.split(".")[0]: file for file in cls.LINKS_DIR.iterdir() if file.is_file()}
    
    @classmethod
    def get_path_dir_data(cls) -> dict[str, Path]:
        return {dir.name : dir  for dir in cls.DATA_PATH.iterdir() if dir.is_dir()}

# classe para gerenciar diretório e seus arquivos
class DirManager():
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path
    
    def list_dir(self)->dict[str, Path]:
        return {dir.name : dir  for dir in self.dir_path.iterdir() if dir.is_dir()}
    def list_file(self)->dict[str, Path]:
        return {file.name.split(".")[0]: file for file in self.dir_path.iterdir() if file.is_file()}


if __name__ == "__main__":
    print(Config.get_path_dir_data())
    directory = DirManager(Config.get_path_dir_data()["microdados_enem_2023"])
    print(directory.list_dir()) 
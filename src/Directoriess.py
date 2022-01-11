import os, sys

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# )
from src.Constants.Constantes import CARPETA_DATA_NAME


# CARPETA_DATA_NAME = "data"
class Directoriess:
    def __init__(self, carpeta: str = CARPETA_DATA_NAME) -> None:
        self.carpeta = carpeta
        self.currentPath = os.getcwd()

    def create_folder(self, carpeta=None) -> bool:
        carpeta = carpeta if carpeta else self.carpeta
        ruta: str = os.path.join(self.currentPath, carpeta)

        if not os.path.exists(ruta):
            os.makedirs(ruta)
            return True

        return False

    def path_actual(self) -> str:
        return self.currentPath

    def exists_file(self, filename: str) -> bool:
        filename = filename if filename else self.filename

        ruta = os.path.join(self.currentPath, self.carpeta, filename)
        return os.path.isfile(ruta)

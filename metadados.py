import os
from pathlib import Path

class Metadados: 
    def __init__(self, repository): 
        if not os.path.exists(repository):
            raise FileNotFoundError(f"O arquivo {self.__arquivo} não existe.")
        
        self.__arquivo = Path(repository)
        
        
    def tamanho(self): 
        """
        Retorna o tamanho do arquivo ou pasta.
        """
        return self.__arquivo.stat().st_size

    def ultimaModificacao(self): 
        """
        Retorna a última modificação do arquivo ou pasta.
        """
        return self.__arquivo.stat().st_mtime

    def extensao(self): 
        """
        Retorna a extensão do arquivo ou pasta.
        """
        if self.__arquivo.is_dir():
            return "diretório"
        return self.__arquivo.suffix
    
    def nome(self):
        """
        Retorna o nome do arquivo ou pasta.
        """
        return self.__arquivo.name

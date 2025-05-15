import os, shutil

class Command: 
    @staticmethod
    def copiarConteudo(src, dest):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
        return True
     
    @staticmethod
    def copiarDimanicamente(src: str, dest: str, arquivo: str):        
        diferenca = arquivo.split(src)[1].split("/")        
        
        for dif in diferenca[1:-1]:
            if not os.path.exists(os.path.join(dest, dif)):
                os.mkdir(os.path.join(dest, dif))
                
            dest = os.path.join(dest, dif)
            
        shutil.copy2(arquivo, dest)
        
    @staticmethod
    def remover(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            print("Arquivo ou pasta nao encontrado")
        
    @staticmethod
    def searchFile( path, file):
        for root, _, files in os.walk(path):
            if file in files:
                return os.path.join(root, file)
        return False
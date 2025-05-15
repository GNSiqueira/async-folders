import json 
from hash import Hash, os
from comands import Command

class Persistencia:    
    def __init__(self):
        self.persistenceConfig = self.__fileConfig()
    
    def __fileConfig(self):
        file = "persistence"
        repository = os.path.join(self.__repositoryComputer(), file)
        
        if not os.path.exists(repository):
            with open(repository, 'w') as f:
                json.dump([], f, indent=4)
                print("Arquivo criado com sucesso")
        return repository
    
    def __repositoryComputer(self):
        try: 
            if os.name == 'nt':  # Windows
                repository = os.path.join(os.getenv('APPDATA'), 'async_folders')
            else:  # Unix (Linux, macOS)
                repository = os.path.join(os.path.expanduser('~'), '.config', 'async_folders')
                        
            if not os.path.exists(repository):
                os.makedirs(repository)
                print("Pasta criada com sucesso")
            
        except:
            raise False
        return repository

    def async_folder_init(self, repository1, repository2): 
        async_dir = os.path.join(repository1, ".async")

        if os.path.exists(async_dir):
          Command.remover(async_dir)
            
        print("Pasta .async criada com sucesso")
        os.mkdir(async_dir)

        estrutura = self.estruturaHash(repository1)
        self.salvar(estrutura, os.path.join(async_dir, "estrutura.json"))
        
        Command.copiarConteudo(repository1, repository2)
        
        async_dir2 = os.path.join(repository2, ".async")
        Command.remover(async_dir2)
        os.mkdir(async_dir2)
        estrutura2 = self.estruturaHash(repository2)
        self.salvar(estrutura2, os.path.join(async_dir2, "estrutura.json"))
        

    def salvarComputer(self, dados):
        try: 
            with open(self.persistenceConfig, 'w') as f:
                json.dump(dados, f, indent=4)
        except Exception as e:
            print(e)
            return False
        return True

    def salvar(self, dados, repository):
        try: 
            with open(repository, 'w') as f:
                json.dump(dados, f, indent=4)
        except Exception as e:
            print(e)
            return False
        return True
      
    def carregarComputador(self) -> list:
        try: 
            if not os.path.isfile(self.persistenceConfig):
                print("Arquivo nao encontrado")
                return False
            
            with open(self.persistenceConfig, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
            return False
        return True
    
    def carregar(self, path) -> list:
        try: 
            if not os.path.isfile(path):
                print("Arquivo nao encontrado")
                return False
            
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
            return False
        return True
               
    def estruturaHash(self, caminho_pasta) -> dict:
        estrutura = {}
        for raiz, pasta, arquivo in os.walk(caminho_pasta):
            if ".async" in pasta:
                pasta.remove(".async")
            
            for folder in pasta:
                estrutura[folder] = [Hash.calcular_hash_folder(os.path.join(raiz, folder)), raiz, "folder"]
                
            for file in arquivo:
                estrutura[file] = [Hash.calcular_hash_file(os.path.join(raiz, file)), raiz, "file"]
        return estrutura
    
    def searchPathInAsync(self, path, path_async): 
        sync = self.carregar(path_async)
        
        if path not in sync: 
            return False
        
        return sync[path]
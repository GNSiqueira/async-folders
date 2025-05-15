import hashlib
import os, json

def print_json(dado):
    print(json.dumps(dado, indent=4, ensure_ascii=False))

class Hash:
    @staticmethod
    def calcular_hash_file(caminho_arquivo) -> str:
        """
        Calcula o hash SHA-1 de um arquivo.
        """
        
        if not isinstance(caminho_arquivo, str):
            return 1, "O caminho do arquivo deve ser uma string."
        
        if os.path.isdir(caminho_arquivo):
            return 2, "O arquivo não existe."
        
        with open(caminho_arquivo, 'rb') as f:
            conteudo = f.read()
        header = f"blob {len(conteudo)}\0".encode('utf-8')
        dados = header + conteudo
        return hashlib.sha1(dados).hexdigest()

    @staticmethod
    def calcular_hash_folder(caminho_pasta) -> str:
        if not isinstance(caminho_pasta, str):
            return "Erro: o caminho deve ser uma string."
        
        if not os.path.isdir(caminho_pasta):
            return "Erro: o caminho não é uma pasta."

        hash_total = hashlib.sha1()

        for raiz, _, arquivos in os.walk(caminho_pasta):
            for nome_arquivo in sorted(arquivos):
                caminho_completo = os.path.join(raiz, nome_arquivo)

                # Adiciona o caminho relativo para garantir que a estrutura da pasta influencia o hash
                caminho_relativo = os.path.relpath(caminho_completo, caminho_pasta)
                hash_total.update(caminho_relativo.encode())

                # Adiciona o conteúdo do arquivo
                with open(caminho_completo, 'rb') as f:
                    while True:
                        bloco = f.read(4096)
                        if not bloco:
                            break
                        hash_total.update(bloco)

        return hash_total.hexdigest()

    @staticmethod
    def validade_hash(hash, path):
        """
        Verifica se o hash de um path é válido.
        """
        if path == "":
            return 1, "O path não existe."
        
        if os.path.isdir(path): 
            hash_path = Hash.calcular_hash_folder(path)
        else: 
            hash_path = Hash.calcular_hash_file(path)
            
        
        print(hash_path)
        print(hash)
    
    
    
        if hash_path != hash:
            return False
        
        return True

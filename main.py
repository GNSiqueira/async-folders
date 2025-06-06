from comands import Command
from metadados import Metadados
from persistense import Persistencia, os
import sys, time
from hash import Hash


config = Persistencia()


def ativar_syncs(): 
    dados = config.carregarComputador()
    
    for index, dado in enumerate(dados):
        resp = validar_existensia(dado)
        def temp():
            if not resp is True: 
                print("\nDeseja ativar essa sincronização?")
                print(f"\t{dado[0]} \n\t  {dado[1]} \nStatus de Sincronia: {"ON" if dado[2] else "OFF"}")
                inp = input("Clique no ENTER para não ou digite \"Y\" para ativar: ")
                if inp.lower() == "y": 
                    d = config.carregarComputador()
                    d[index][2] = True
                    config.salvarComputer(d) 
                elif inp == "": 
                    pass
                else: 
                    limpar_tela()
                    print("Resposta não identificada!")
                    temp()
        temp()                  
        
def add_sync_folder(folder1, folder2, indice): 
    print("\nPasta nao encontrada!")
    print("\nProblema ao pesquisar pastas: \n\t" + folder1 + "\n\t" + folder2)
    print("\nSelecione uma das opções abaixo: ")
    print("1 - Apagar essa sincronização")
    print("2 - Apenas preciso conectar meu dispositivo")
    print("3 - Resincronizar as pastas")
    print("4 - Apenas continue")
    print("Clique no ENTER para ignorar essa sincronização.")
    selection = input("\nSelecione uma opção: ")
    
    if selection == "1":
        remove_sync(indice)
        return False
    elif selection == "2":
        return False
    elif selection == "3":
            if not os.path.exists(folder1):
                if not os.path.exists(folder2):
                    print("Ambas as pastas nao foram encontradas!")
                    print("Selecione as pastas novamente:")
                    folder1 = input("Pasta 1: ")
                    folder2 = input("Pasta 2: ")
                    
                    if not os.path.exists(folder1) and not os.path.exists(folder2):
                        print("Ambas as pastas nao foram encontradas!")
                        return False
                    
                    before = config.carregarComputador()
                    before[indice] = [folder1, folder2, True]
                    config.salvarComputer(before)
                    config.salvar(config.estruturaHash(folder1), os.path.join(folder1, ".async", "estrutura.json"))
                    config.salvar(config.estruturaHash(folder2), os.path.join(folder2, ".async", "estrutura.json"))
                    
                    return sync_folders(folder1, folder2, indice)
                
                else:
                    print("Pasta 1 nao foi encontrada!")
                    print("Selecione a pasta novamente:")
                    folder1 = input("Pasta 1: ") 
                    
                    if not os.path.exists(folder1):
                        print("Pasta nao encontrada!")
                        return False
                    
                    before = config.carregarComputador()
                    before[indice] = [folder1, folder2, True]
                    config.salvarComputer(before)
                    config.salvar(config.estruturaHash(folder1), os.path.join(folder1, ".async", "estrutura.json"))

                    
                    return sync_folders(folder1, folder2, indice)
                                
            elif not os.path.exists(folder2):
                print("Pasta 2 nao foi encontrada!")
                print("Selecione a pasta novamente:")
                folder2 = input("Pasta 2: ") 
                
                if not os.path.exists(folder2):
                    print("Pasta nao encontrada!")
                    return False
                
                before = config.carregarComputador()
                before[indice] = [folder1, folder2, True]
                config.salvarComputer(before)
                config.salvar(config.estruturaHash(folder2), os.path.join(folder2, ".async", "estrutura.json"))

                
                return sync_folders(folder1, folder2, indice)

            else:
                print("Opção inválida!")
                return False

    elif selection == "4": 
        before = config.carregarComputador()
        before[indice] = [folder1, folder2, True]
        config.salvarComputer(before)
        return True

    else: 
        before = config.carregarComputador()
        before[indice] = [folder1, folder2, False]
        config.salvarComputer(before)
        return False
    

def validar_existensias(): 
    dados = config.carregarComputador()
    
    for index, dado in enumerate(dados):
        dado[2] = True
        resp = validar_existensia(dado)
        if resp == 0: 
            add_sync_folder(dado[0], dado[1], index)
        if resp == 2:
            d = config.carregarComputador()
            d[index][2] = True
            config.salvarComputer(d) 
        
            
        limpar_tela()

def validar_existensia(dado): 
    """
    + Validar se as pastas existem
        + Se as duas existirem não fazer nada
        + Se as duas não existirem, perguntar se o usuário deseja adicionar uma nova sincronização, ou apenas ignorar
            + Caso ele deseje ignorar, alterar os dois ultimos parametros da config para False.
            + Caso ele deseje adicionar uma nova sincronização, chamar a função add_new_sync com o index para fazer a alteração.
        + Se apenas a primeira existir perguntar se o usuário deseja adicionar uma nova sincronização, ou apenas ignorar
            + Caso ele deseje ignorar
        + Se apenas a segunda existir perguntar se o usuário deseja adicionar uma nova sincronização, ou apenas ignorar
    
    return 0 Ele está sendo rastreado mas as pastas não existem
    return 1 # Nao era para ele estar sendo rastreado
    return 2 # Era para ele estar sendo rastreado
    return True # #Está tudo certo
    
    """
    
    folder1 = dado[0]
    folder2 = dado[1]
    folder1Existense = dado[2]
    
    if not os.path.exists(folder1) or not os.path.exists(folder2):
        if folder1Existense == True:
            return 0 # Ele está sendo rastreado mas as pastas não existem
        else: 
            return 1 # Nao era para ele estar sendo rastreado
    elif folder1Existense == False:
        return 2 # Era para ele estar sendo rastreado
        
    return True # #Está tudo certo

def main(): 
    print("*" * 40)
    print("    📁 MENU DE OPÇÕES - Sync Folders     ")
    print("*" * 40)
    print("1 - Adicionar nova sincronização")
    print("2 - Remover sincronização")
    print("3 - Listar sincronizações")
    print("4 - Sincronizar agora")
    print("5 - Sincronização automática")
    print("6 - Ativar sincronizações")
    print("0 - Sair ou Ctrl + C")
    print("*" * 40)
    
    return input("Escolha uma opção: ")
  
def add_new_sync(fold1 = None, fold2 = None):
    """
    Adiciona uma nova sincronização
    """
    if fold1 == None and fold2 == None:
        primeira_pasta = input("\nDigite o caminho da primeira pasta: ")
        segunda_pasta = input("Digite o caminho da segunda pasta: ")
    else: 
        primeira_pasta = fold1
        segunda_pasta = fold2
        
    try: 
        if primeira_pasta == "" or segunda_pasta == "":
            print("Preencha todos os campos!")
            if fold1 != None and fold2 != None:
                add_new_sync(fold1, fold2)
                
            add_new_sync()
            return
            
        if primeira_pasta == segunda_pasta:
            print("As pastas não podem ser iguais!")
            if fold1 != None and fold2 != None:
                add_new_sync(fold1, fold2)
                
            add_new_sync()
            return
        
        if not os.path.isdir(primeira_pasta) or not os.path.isdir(segunda_pasta):
            print("Alguma das pastas não existe!")
            if fold1 != None and fold2 != None:
                add_new_sync(fold1, fold2)
                
            add_new_sync()
            return
        
        before = config.carregarComputador()
            
        new = [primeira_pasta, segunda_pasta, True]

        if new in before or [segunda_pasta, primeira_pasta] in before:
            if os.path.exists(os.path.join(primeira_pasta, ".async")) and os.path.exists(os.path.join(segunda_pasta, ".async")):
                print("Essa sincronização já existe!")
                return

        
        if len(os.listdir(primeira_pasta)) > 0 and len(os.listdir(segunda_pasta)) == 0:
            config.async_folder_init(primeira_pasta, segunda_pasta)
        elif len(os.listdir(segunda_pasta)) > 0 and len(os.listdir(primeira_pasta)) == 0:
            config.async_folder_init(segunda_pasta, primeira_pasta)
        elif len(os.listdir(primeira_pasta)) == 0 and len(os.listdir(segunda_pasta)) == 0:
            print("Ambas as pastas estão vazias!")
            return
        elif len(os.listdir(primeira_pasta)) > 0 and len(os.listdir(segunda_pasta)) > 0:
            print("\nAmbas as pastas estão cheias!")
            print("Selecione uma das opções abaixo para apagar: ")
            print("1 - Apagar a primeira pasta: " + primeira_pasta)
            print("2 - Apagar a segunda pasta: " + segunda_pasta)
            print("3 - Cancelar")
            
            selection = input("Selecione uma opção: ")
            if selection == "1":
                Command.remover(primeira_pasta)
                os.mkdir(primeira_pasta)
                config.async_folder_init(segunda_pasta, primeira_pasta)
            elif selection == "2":
                Command.remover(segunda_pasta)
                os.mkdir(segunda_pasta)
                config.async_folder_init(primeira_pasta, segunda_pasta)
            else:
                return
            
            
        
        before.append(new)
        
        if fold1 == None and fold2 == None:
            config.salvarComputer(before)
        
        print("Sincronização adicionada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao adicionar sincronização: {e}")
        return
                
def remove_sync(indice = None):
    """
    Remove uma sincronização
    """
    lista = config.carregarComputador()
    
    if indice == None:
        if len(lista) == 0:
            print("Nenhuma sincronização encontrada!")
            return
        
        list_sync()
        selection = input("Selecione um numero para remover: ")
    else: 
        selection = indice + 1
    try: 
        selection = int(selection)
    except ValueError:
        print("Seleção inválida!")
        return

    if selection < 1 or selection > len(lista): 
        print("Seleção inválida!")
        return
    
    lista.pop(selection - 1)
    config.salvarComputer(lista)
    print("Sincronização removida com sucesso!")
    return
                
def list_sync():
    """
    Lista as sincronizações
    """
    for number, sync in  enumerate(config.carregarComputador()):
        print(f"\nSincronização {number + 1} : {sync[0]} \n\t\t  {sync[1]} \nStatus de Sincronia: {"ON" if sync[2] else "OFF"}")
    print("")
  
def sync_now():
    """
    Sincroniza agora
    """
    folders = config.carregarComputador()
    if len(folders) == 0:
        print("Nenhuma sincronização encontrada!")
        return
    for index, folder in enumerate(folders):
        resp = validar_existensia(folder)
        
        if resp == 0: 
            if not add_sync_folder(folder[0], folder[1], index): 
                continue
        elif resp is True:
            pass
        elif resp == 1: 
            continue
        elif resp == 2: 
            d = config.carregarComputador()
            d[index][2] = True
            config.salvarComputer(d) 
            
        if sync_folders(folder[0], folder[1]):
            folder = config.carregarComputador()[index]
            if sync_folders(folder[1], folder[0]): 
                config.salvar(config.estruturaHash(folder[0]), os.path.join(folder[0], ".async", "estrutura.json"))
                config.salvar(config.estruturaHash(folder[1]), os.path.join(folder[1], ".async", "estrutura.json"))
    
def sync_folders(folder1, folder2):
    """
    Sincroniza agora
    """
    
    pathSync = os.path.join(folder1, ".async", "estrutura.json")
    pathSync2 = os.path.join(folder2, ".async", "estrutura.json")
    
    if not os.path.exists(pathSync): 
        if os.path.exists(pathSync2):
            Command.remover(folder1)
            os.mkdir(folder1)
            Command.copiarConteudo(folder2, folder1)
            config.salvar(config.estruturaHash(folder1), os.path.join(folder1, ".async", "estrutura.json"))
            return True
        else:
            print("\nUma pasta chamada (.async) nao foi encontrada!\nIremos adicionar a sincronização novamente.\nAdicionar sincronização...")
            add_new_sync(folder1, folder2)
            return True
        
    elif not os.path.exists(pathSync2):
        Command.remover(folder2)
        os.mkdir(folder2)
        Command.copiarConteudo(folder1, folder2)
        config.salvar(config.estruturaHash(folder2), os.path.join(folder2, ".async", "estrutura.json"))
        return True
                
    for root, _, files in os.walk(folder1):
        if root == os.path.join(folder1, ".async"): continue
        for file in files:
            file2 = Command.searchFile(folder2, file)
            if file2: 
                info1 = Hash.calcular_hash_file(os.path.join(root, file))
                info2 = Hash.calcular_hash_file(file2)
                if not info1 == info2:
                    info1 = Metadados(os.path.join(root, file)).ultimaModificacao()
                    info2 = Metadados(file2).ultimaModificacao()
                    if info1 > info2: 
                        Command.remover(file2)
                        Command.copiarDimanicamente(folder1, folder2, os.path.join(root, file))
                        continue
                    elif info1 < info2:
                        Command.remover(os.path.join(root, file))
                        Command.copiarDimanicamente(folder2, folder1, file2)
                        continue
                infoo = config.searchPathInAsync(file, pathSync)
                if infoo:
                    if root != infoo[1]:
                        Command.remover(os.path.join(file2))
                        Command.copiarDimanicamente(folder1, folder2, os.path.join(root, file))
                    continue
                Command.copiarDimanicamente(folder1, folder2, os.path.join(root, file))
                continue
            else: 
                infoFile2 = config.searchPathInAsync(file, pathSync2)
                if infoFile2: 
                    infoFile = config.searchPathInAsync(file, pathSync)
                    if not Hash.validade_hash(infoFile[0], os.path.join(root, file)):
                        Command.copiarDimanicamente(folder1, folder2, os.path.join(root, file))
                        continue
                    else: 
                        Command.remover(os.path.join(root, file))
                        continue
                else: 
                    Command.copiarDimanicamente(folder1, folder2, os.path.join(root, file))
                    continue
    return True

def auto_sync():
    """
    Sincronização automática
    """
    while True:
        sync_now()
        time.sleep(30)

def escolha(opcao):
    """
    1 - Adicionar nova sincronização *certo*
    2 - Remover sincronização 
    3 - Listar sincronizações *certo*
    4 - Sincronizar agora
    5 - Sicronização automática
    6 - Sair
    """

    try: 
        if opcao == "1":
            print("\nAdicionando nova sincronização...")
            print("Precione Ctrl + C para cancelar e voltar para o MENU.")
            add_new_sync()
        elif opcao == "2":
            print("\nRemovendo sincronização...")
            print("Precione Ctrl + C para cancelar e voltar para o MENU.")
            remove_sync()
        elif opcao == "3":
            print("\nListando sincronizações...")
            print("Precione Ctrl + C para cancelar e voltar para o MENU.")
            list_sync()
        elif opcao == "4":
            print("\nSincronizando agora...")
            print("Precione Ctrl + C para cancelar e voltar para o MENU.")
            sync_now()
        elif opcao == "5":
            print("\nSincronização automática...")
            print("Precione Ctrl + C para cancelar e voltar para o MENU.")
            auto_sync()
        elif opcao == "6":
            print("\nAtivar sincronizações de pastas...")
            print("Precione Ctrl + C para cancelar e voltar para o MENU.")
            ativar_syncs()
        else:
            print("Opção inválida!")
    except KeyboardInterrupt: 
        print("\n\nInterrompido pelo usuário!\nVoltando para o MENU...")

    input("Pressione Enter para continuar...")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    try:
        limpar_tela()
        validar_existensias()
        while True:
            limpar_tela()
            opcao = main()
            
            if opcao == "0":
                print("\nSaindo do programa...\n")
                sys.exit(0)
                break
            
            escolha(opcao)
    except KeyboardInterrupt:
        print("\n\nSaindo do programa...\n")
        sys.exit(0)
    
if __name__ == "__main__":
    menu()
  
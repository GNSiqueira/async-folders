# 🔄 SyncFolders - Sincronização Bidirecional entre Pastas
Um projeto de sincronização bidireciona em python. Apenas com interface no terminal.

**SyncFolders** é um utilitário em Python que realiza sincronização bidirecional entre duas pastas locais, mantendo os arquivos atualizados entre elas. O sistema detecta arquivos novos, modificados e até mesmo deletados — garantindo que ambas as pastas estejam sempre espelhadas.

---

## 🚀 Funcionalidades

- ✅ Sincronização bidirecional entre duas pastas
- 🕵️‍♂️ Detecção de:
  - Arquivos novos
  - Arquivos modificados
  - Arquivos deletados
- 🧠 Registro de estado anterior para rastreamento inteligente
- 🧹 Evita loops de sincronização (ex: não copia a pasta destino para dentro dela mesma)
- ⏱️ Suporte a sincronização automática por intervalo (opcional)
- 📁 Menu de linha de comando simples e intuitivo

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/GNSiqueira/async-folders.git
cd syncfolders
python main.py


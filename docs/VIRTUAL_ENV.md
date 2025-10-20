# 🐍 AMBIENTE VIRTUAL E DEPENDÊNCIAS

## 📋 Status Atual

✅ **Ambiente Virtual**: Criado em `.venv/`  
❌ **SSL/TLS**: Não disponível no Python atual  
❌ **pyserial**: Não instalado (devido ao SSL)  
❌ **PyQt5**: Não instalado (devido ao SSL)  

## 🚀 Como Usar (3 Opções)

### Opção 1: Universal Uploader (🥇 RECOMENDADA)
```bash
# Sempre funciona - com ou sem dependências
python universal_uploader.py
```
**Funcionalidades:**
- ✅ Modo simulação quando pyserial não disponível  
- ✅ Modo completo quando pyserial instalado  
- ✅ Interface clara e intuitiva  
- ✅ Todas as funcionalidades de upload  

### Opção 2: Terminal Uploader (Básico)
```bash
# Versão original
python terminal_uploader.py
```

### Opção 3: Interface Gráfica (Requer PyQt5)
```bash
# Só funciona com PyQt5 instalado
python simple_pico_uploader.py
```

## 🔧 Ambiente Virtual

### Ativar/Desativar
```bash
# Ativar
source .venv/bin/activate

# Ou usar script criado
./activate.sh

# Desativar  
deactivate
```

### Scripts de Conveniência Criados
```bash
./activate.sh     # Ativa ambiente virtual
./run.py         # Executa uploader automaticamente
python check_env.py  # Verifica status completo
```

## 🛠️ Resolução de Problemas SSL

### Problema
O Python atual foi compilado sem suporte SSL/TLS completo, impedindo:
- Instalação via pip de pacotes do PyPI
- Download automático de dependências

### Soluções

#### 1. Instalar Python via Homebrew (Recomendado)
```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python com SSL
brew install python

# Recriar ambiente virtual
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install pyserial PyQt5
```

#### 2. Usar pyenv para gerenciar Python
```bash
# Instalar pyenv
brew install pyenv

# Instalar Python via pyenv
pyenv install 3.11.6
pyenv local 3.11.6

# Recriar ambiente
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install pyserial PyQt5
```

#### 3. Download Manual (Mais Trabalhoso)
```bash
# Baixar pyserial manualmente
curl -L -o pyserial.tar.gz https://files.pythonhosted.org/packages/1e/7d/ae3f0a63f41e4d2f6cb66a5b57197850f919f59e558159a4dd3a818f5082/pyserial-3.5.tar.gz

# Extrair e instalar
tar -xzf pyserial.tar.gz
cd pyserial-3.5
python setup.py install
```

## 📊 Status das Aplicações

| Aplicação | Status | Funciona Sem pyserial | Funciona Sem PyQt5 |
|-----------|--------|----------------------|-------------------- |
| `universal_uploader.py` | ✅ | ✅ (modo simulação) | ✅ |
| `terminal_uploader.py` | ⚠️ | ❌ | ✅ |
| `simple_pico_uploader.py` | ❌ | ❌ | ❌ |
| `pico_uploader.py` | ❌ | ❌ | ❌ |

## 🎯 Recomendação Final

### Para Uso Imediato
```bash
python universal_uploader.py
```
- Funciona **agora** mesmo sem dependências
- Modo simulação para testar interface  
- Modo completo quando pyserial disponível

### Para Desenvolvimento Completo
1. Instale Python via Homebrew ou pyenv
2. Recrie ambiente virtual com SSL funcionando
3. Instale todas as dependências
4. Use qualquer aplicação do projeto

## 🆘 Suporte

### Verificar Status
```bash
python check_env.py  # Status completo do ambiente
```

### Teste Rápido
```bash
# Sempre funciona
python universal_uploader.py

# Testa SSL
python -c "import ssl; print('SSL OK')"

# Testa pyserial  
python -c "import serial; print('pyserial OK')"
```

---

**💡 O universal_uploader.py foi criado especificamente para resolver o problema das dependências e funcionar em qualquer situação!**
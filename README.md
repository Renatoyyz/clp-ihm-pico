# CLP-IHM-PICO - Sistema LADDER para Raspberry Pi Pico

Sistema completo de desenvolvimento para Raspberry Pi Pico com **Interface LADDER Visual** e ferramentas de upload/comunicação.

## 🎯 Funcionalidades Principais

### 🖥️ **Interface LADDER Visual (Nova!)**
- ✅ **Interface gráfica PyQt5** profissional
- ✅ **Conexão avançada com Pico** (detecção automática)
- ✅ **Monitor em tempo real** da comunicação
- ✅ **Console interativo** com comandos de teste
- ✅ **Layout responsivo** com painéis redimensionáveis
- 🔲 **Editor visual LADDER** (próxima fase)

### � **Terminal Uploader (Estável)**
- ✅ **Upload de arquivos Python** (.py) para o Pico
- ✅ **Execução automática** após upload
- ✅ **Reset remoto** do Pico (soft/hard)
- ✅ **Lista arquivos** no Pico
- ✅ **Compatível** com Pico, Pico W, Pico 2 e Pico 2 W
- ✅ **Funciona sem dependências** (modo simulação)

## 🚀 Como Executar

### Interface LADDER (Recomendado)
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar interface gráfica
cd interface_ladder
python3 app.py
```

### Terminal Uploader (Alternativo)
```bash
# Funciona sem dependências
python3 main.py
```

### Opção 3: Instalação Completa

```bash
# Com Homebrew (para resolver SSL)
brew install python
pip3 install pyserial PyQt5

# Ou execute o script de setup
./setup_venv.sh
```

## 📁 Estrutura do Projeto

```
clp-ihm-pico/
├── 🖥️ interface_ladder/        # Interface LADDER Visual (Nova!)
│   ├── app.py                 # Aplicação principal
│   ├── main_window.py         # Janela principal
│   ├── config_dialog.py       # Configuração do Pico (FUNCIONAL)
│   ├── run.py                 # Script de inicialização
│   └── README.md              # Documentação da interface
│
├── 🔧 src/                    # Código principal estável
│   └── universal_uploader.py  # Terminal uploader universal
│
├── 🧪 tests/                  # Testes e utilitários
│   ├── test_dependencies.py   # Teste de dependências
│   └── ...
│
├── 📚 legacy/                 # Versões anteriores
│   ├── terminal_uploader.py   # Terminal básico
│   ├── simple_pico_uploader.py # PyQt5 simples
│   └── ...
│
├── 🥧 pico_examples/          # Exemplos para Pico
│   ├── blink_led.py          # LED piscante
│   ├── ladder_example.py     # Exemplo LADDER
│   └── ...
│
├── 📖 docs/                   # Documentação
├── 🛠️ scripts/               # Scripts auxiliares
├── main.py                   # Entry point principal
├── test_dependencies.py     # Teste rápido
└── README.md                 # Este arquivo
```

## 🎮 Como Usar

### 🖥️ **Interface LADDER (Recomendado)**

```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate

# 2. Executar interface
cd interface_ladder
python3 app.py
```

**Funcionalidades disponíveis:**
- ✅ **Conexão avançada**: Menu Configurações → Conexão Pico
- ✅ **Detecção automática** de Raspberry Pi Pico
- ✅ **Monitor em tempo real** da comunicação
- ✅ **Comandos de teste** pré-definidos
- ✅ **Console interativo** para comandos personalizados

### 🔧 **Terminal Uploader (Backup)**

```bash
# Funciona sem dependências
python3 main.py
```

### 2. **Conectar ao Pico**

#### Interface LADDER:
1. Menu **"Configurações"** → **"Conexão Pico"**
2. Aguarde detecção automática (ícone 🥧 aparece nos Picos)
3. Clique **"Conectar"** ou ative **"Conectar automaticamente"**

#### Terminal:
1. Escolha opção **"2"** (Conectar ao Pico)
2. Selecione a porta na lista
3. Conexão estabelecida automaticamente

### 3. **Upload e Execução**

```bash
# No terminal uploader
Opção 3R: Upload + Executar arquivo
```

**Interface LADDER** (próxima fase): Editor visual de arrastar e soltar
├── install.sh                  # Script de instalação
└── README.md                   # Este arquivo
```

## 🔧 Funcionalidades das Versões

### 🥇 Versão Terminal (`terminal_uploader.py`) - RECOMENDADA
- ✅ **Sempre funciona** - sem dependências gráficas
- ✅ Interface intuitiva no terminal
- ✅ Upload de arquivos individuais ou pastas
- ✅ Listagem e execução de arquivos
- ✅ Comandos MicroPython personalizados
- ✅ Reset remoto do Pico
- ✅ **Ideal para qualquer sistema**

### Versão Simples (`simple_pico_uploader.py`)
- Interface PyQt5 básica e intuitiva
- Upload de arquivos individuais
- Listagem de arquivos do Pico
- Execução de scripts
- Ideal para uso básico com GUI

### Versão Completa (`pico_uploader.py`)
- Interface PyQt5 avançada
- Upload de múltiplos arquivos
- Upload de pastas inteiras
- Gerenciador de arquivos do Pico
- Barra de progresso
- Console REPL integrado
- Ideal para desenvolvimento avançado

## 🐛 Solução de Problemas

### Problema: "pyserial não instalado" ou "import serial falhou"

**Soluções:**
```bash
# Tente uma dessas opções:
pip3 install pyserial
python -m pip install pyserial
conda install pyserial

# Se nada funcionar, use:
python3 simple_setup.py     # Setup sem dependências
```

### Problema: "Nenhuma porta encontrada"

**Soluções:**
1. Verifique se o Pico está conectado via USB
2. Verifique se o driver USB está instalado
3. No macOS, as portas geralmente aparecem como `/dev/tty.usbmodem*`
4. No Linux, geralmente são `/dev/ttyACM*` ou `/dev/ttyUSB*`
5. No Windows, são `COM*`

### Problema: "Falha na conexão"

**Soluções:**
1. Certifique-se que MicroPython está instalado no Pico
2. Feche outros programas que possam estar usando a porta (Arduino IDE, VS Code, etc.)
3. Tente desconectar e reconectar o Pico
4. Verifique se a velocidade está em 115200 baud

### Problema: "Erro no upload"

**Soluções:**
1. Verifique se há espaço suficiente no Pico
2. Certifique-se que o arquivo não está sendo usado
3. Tente resetar o Pico antes do upload

## 🔮 Próximos Passos para LADDER

Esta aplicação serve como base para implementar um sistema LADDER. Funcionalidades futuras podem incluir:

- **Editor gráfico LADDER** com PyQt5
- **Compilador LADDER para MicroPython**
- **Simulador de I/O** para testes
- **Monitoramento em tempo real** de variáveis
- **Debugger visual** para lógica LADDER

## 📝 Exemplo de Uso com LADDER

```python
# Exemplo de como a lógica LADDER pode ser convertida
# Rung 1: Se INPUT_1 AND INPUT_2 então OUTPUT_1 = True
if pin_input1.value() and pin_input2.value():
    pin_output1.on()
else:
    pin_output1.off()
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- Raspberry Pi Foundation pelo excelente Pico
- Comunidade PyQt5 pela interface gráfica
- Comunidade MicroPython pelo runtime

---

**Desenvolvido para facilitar o desenvolvimento com Raspberry Pi Pico e preparar o terreno para sistemas LADDER embarcados.**
# Raspberry Pi Pico File Uploader

Uma coleção de aplicações para conectar e fazer upload de arquivos para Raspberry Pi Pico (Pico, Pico W, Pico 2, Pico 2 W), similar à funcionalidade da extensão VS Code para Pico.

## 🚀 Funcionalidades

- ✅ **Conecta automaticamente** ao Raspberry Pi Pico via serial
- ✅ **Upload de arquivos Python** (.py) para o Pico
- ✅ **Lista arquivos** no sistema de arquivos do Pico
- ✅ **Executa scripts** diretamente no Pico
- ✅ **Reset remoto** do Pico
- ✅ **Interface gráfica** com PyQt5 (quando disponível)
- ✅ **Interface de terminal** (sempre funciona)
- ✅ **Log em tempo real** das operações
- ✅ **Compatível** com Pico, Pico W, Pico 2 e Pico 2 W
- ✅ **Base para sistema LADDER** futuro

## 📋 Pré-requisitos

1. **Python 3.7+** instalado no sistema
2. **Raspberry Pi Pico** com **MicroPython** instalado
3. **Cabo USB** para conectar o Pico ao computador

### Verificar se o MicroPython está instalado no Pico

1. Conecte o Pico segurando o botão BOOTSEL
2. Arraste o arquivo `pico_micropython.uf2` para o drive que aparece
3. O Pico reiniciará automaticamente com MicroPython

## 🛠️ Instalação

### Opção 1: Uso Imediato (SEM instalação)

```bash
# Funciona AGORA - sem dependências
python3 universal_uploader.py
```

### Opção 2: Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Tentar instalar dependências
pip install pyserial PyQt5

# Se falhar por SSL, use universal_uploader.py
python universal_uploader.py
```

### Opção 3: Instalação Completa

```bash
# Com Homebrew (para resolver SSL)
brew install python
pip3 install pyserial PyQt5

# Ou execute o script de setup
./setup_venv.sh
```

## 🎮 Como Usar

### 1. Executar a Aplicação

#### 🥇 Versão Universal (SEMPRE funciona)
```bash
python3 universal_uploader.py
```

#### Outras Versões
```bash
# Terminal básico
python3 terminal_uploader.py

# Interface gráfica (requer PyQt5)
python3 simple_pico_uploader.py
```

### 2. Conectar ao Pico

1. Conecte o Raspberry Pi Pico via USB
2. Na aplicação, clique em **"Atualizar"** para listar portas
3. Selecione a porta do Pico na lista
4. Clique em **"Conectar"**

### 3. Upload de Arquivos

1. Clique em **"Selecionar Arquivo .py"**
2. Escolha o arquivo Python que deseja enviar
3. Clique em **"Upload para Pico"**
4. Aguarde a confirmação no log

### 4. Funcionalidades Adicionais

- **Listar Arquivos**: Vê todos os arquivos no Pico
- **Executar main.py**: Executa o arquivo principal
- **Reset Pico**: Reinicia o microcontrolador

## 📁 Estrutura do Projeto

```
clp-ihm-pico/
├── terminal_uploader.py         # 🥇 Versão terminal (RECOMENDADA)
├── simple_pico_uploader.py      # Interface PyQt5 simples
├── pico_uploader.py            # Interface PyQt5 completa
├── ladder_example.py           # Exemplo de lógica LADDER
├── ladder_editor_concept.py    # Conceito do editor LADDER
├── blink.py                    # Código de exemplo para teste
├── requirements.txt            # Dependências Python
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
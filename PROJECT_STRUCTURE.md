# 🥧 CLP-IHM-PICO PROJECT
# =====================

## 📁 Estrutura do Projeto

```
clp-ihm-pico/
├── main.py                 # ← Ponto de entrada principal
├── run.py                  # ← Script de execução alternativo  
├── README.md               # ← Documentação principal
├── requirements.txt        # ← Dependências Python
├── 
├── src/                    # ← Código fonte principal
│   └── universal_uploader.py   # Aplicação principal de upload
├── 
├── pico_examples/          # ← Exemplos para Raspberry Pi Pico
│   ├── blink_led.py           # Exemplo básico LED
│   ├── button_led.py          # Exemplo botão + LED
│   ├── ladder_*.py            # Exemplos LADDER logic
│   └── main.py               # Programa principal do Pico
├── 
├── tests/                  # ← Testes e experimentos
│   ├── test_communication.py # Testes de comunicação serial
│   ├── test_methods.py       # Testes de métodos de upload
│   └── test_*.py            # Outros testes
├── 
├── legacy/                 # ← Versões antigas (referência)
│   ├── terminal_uploader.py  # Versão terminal simples
│   ├── simple_pico_uploader.py # Versão PyQt5 simples
│   └── pico_uploader.py      # Versão PyQt5 avançada
├── 
├── scripts/                # ← Scripts de setup e utilitários
│   └── (scripts de configuração se houver)
├── 
├── docs/                   # ← Documentação adicional
│   └── (documentos técnicos se houver)
├── 
├── .venv/                  # ← Ambiente virtual Python
└── .vscode/               # ← Configurações VS Code
```

## 🚀 Como Executar

### Método Principal:
```bash
python main.py
```

### Método Alternativo:
```bash
python run.py
```

### Com ambiente virtual:
```bash
source .venv/bin/activate
python main.py
```

## 📋 Próximos Passos

Este projeto está pronto para continuar com:
- [ ] Interface PyQt5 
- [ ] Sistema LADDER Logic
- [ ] Editor gráfico de LADDER
- [ ] Expansão de funcionalidades

## ✅ Status Atual

- ✅ Upload de arquivos para Pico funcionando
- ✅ Execução automática após upload
- ✅ Reset do Pico
- ✅ Detecção de portas corrigida
- ✅ Comunicação REPL estável
- ✅ Estrutura de projeto organizada
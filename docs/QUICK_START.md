# 🚀 INÍCIO RÁPIDO - Raspberry Pi Pico Uploader

## ⚡ 3 Passos para Começar

### 1. 📋 Pré-requisitos Mínimos
- ✅ Python 3.7+ 
- ✅ Raspberry Pi Pico com MicroPython
- ✅ Cabo USB

### 2. 🎯 Execução Imediata
```bash
# Execute isto agora:
python3 terminal_uploader.py
```

### 3. 🔄 Fluxo Básico
1. **Listar portas** (opção 1)
2. **Conectar** ao Pico (opção 2)  
3. **Upload** arquivo ou pasta (opção 3 ou 4)
4. **Executar** no Pico (opção 6)

---

## 📁 Arquivos Principais

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| `terminal_uploader.py` | 🥇 **Interface terminal** | **SEMPRE** - funciona sem GUI |
| `simple_pico_uploader.py` | Interface PyQt5 básica | Quando PyQt5 disponível |
| `examples/` | Códigos de exemplo | Para testar funcionalidades |

---

## 🔧 Instalação de Dependências (Opcional)

```bash
# Para interface gráfica (opcional):
pip3 install pyserial PyQt5

# Ou usar o script automático:
./install.sh
```

**⚠️ IMPORTANTE:** A versão terminal funciona SEM dependências!

---

## 🧪 Arquivos de Teste Incluídos

- `examples/blink_led.py` - Piscar LED onboard
- `examples/button_led.py` - Botão + LED  
- `examples/ladder_basic.py` - Lógica LADDER básica
- `examples/main.py` - Menu principal
- `examples/boot.py` - Configuração de boot

---

## 🆘 Solução Rápida de Problemas

### "Nenhuma porta encontrada"
- Verifique conexão USB do Pico
- Confirme que MicroPython está instalado
- No macOS: procure por `/dev/tty.usbmodem*`

### "Falha na conexão"  
- Feche outros programas (Arduino IDE, VS Code)
- Desconecte e reconecte o Pico
- Tente uma porta diferente

### "Erro no upload"
- Verifique espaço no Pico
- Reset o Pico (opção 7)
- Confirme sintaxe do arquivo Python

---

## 🎯 Teste Rápido de 5 Minutos

1. **Execute:** `python3 terminal_uploader.py`
2. **Conecte** ao Pico (opções 1 → 2)
3. **Upload:** `examples/blink_led.py` (opção 3)
4. **Execute:** o arquivo no Pico (opção 6)
5. **Veja** o LED piscando! 🎉

---

## 🔮 Próximos Passos - Sistema LADDER

Este projeto é a **base** para um sistema LADDER completo:

```python
# Futuro: Editor gráfico LADDER → Código MicroPython
if INPUT_1 and INPUT_2:
    OUTPUT_1 = True
    MEMORY_1 = True
```

**Funcionalidades futuras:**
- 🎨 Editor visual LADDER  
- 🔄 Simulador I/O
- 📊 Monitoramento tempo real
- 🐛 Debugger visual

---

## 📞 Suporte e Contribuição

- 🐛 **Problemas?** Abra uma issue
- 💡 **Ideias?** Pull requests bem-vindos
- 📚 **Dúvidas?** Consulte o README.md completo

---

**✨ Desenvolvido para facilitar automação com Raspberry Pi Pico!**
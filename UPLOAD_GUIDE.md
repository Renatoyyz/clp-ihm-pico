# Sistema de Upload para Raspberry Pi Pico

## 🚀 Funcionalidades Implementadas

### Gerenciador de Conexão Global
- **Arquivo**: `pico_connection_manager.py`
- **Classe**: `PicoConnectionManager` (Singleton)
- Gerencia conexão única com o Pico
- Evita múltiplas conexões simultâneas
- Detecta automaticamente se já está conectado

### Melhorias no Diálogo de Conexão
- **Verificação Automática**: Ao abrir o diálogo, verifica se já existe conexão ativa
- **Status Correto**: Exibe status real da conexão (conectado/desconectado)
- **Desconexão Sempre Disponível**: Botão de desconectar fica habilitado se houver conexão

### Sistema de Upload
- **Upload Automático**: Envia `main_.py` renomeado como `main.py` para o Pico
- **Múltiplos Arquivos**: Opção de enviar todos os arquivos gerados ou apenas o main
- **Verificações**: Verifica conexão e existência de código antes do upload
- **Soft Reset**: Opção de reiniciar o Pico após upload

## 📋 Como Usar

### 1. Conectar ao Pico

```
Menu: Pico → Conectar Pico (ou Ctrl+P)
```

1. Abra o diálogo de conexão
2. Selecione a porta do Pico na lista
3. Clique em "🔌 Conectar"
4. Aguarde confirmação de conexão

**Nota**: Se o Pico já estiver conectado, o diálogo mostrará automaticamente o status e permitirá desconectar.

### 2. Gerar Código

```
Menu: Arquivo → Exportar → Python (ou Ctrl+E)
```

1. Configure seu LADDER e RS485
2. Exporte o código Python
3. Arquivos serão salvos em `../generated_code/`

### 3. Fazer Upload

```
Toolbar: 📤 Upload (ou Menu: Pico → Upload para Pico)
```

1. **Se não conectado**: Sistema perguntará se deseja conectar
2. **Se código não gerado**: Sistema oferecerá gerar automaticamente
3. **Escolha arquivos**:
   - 📦 **Todos**: Envia main_.py, lib_rs485.py, lib_ihm.py, config.json
   - 📄 **Apenas main_.py**: Envia só o código principal
4. **Aguarde**: Upload é feito em chunks de 128 bytes
5. **Soft Reset**: Opção de reiniciar o Pico após upload

## 🔧 Arquivos Enviados

| Arquivo Local | Nome no Pico | Descrição |
|---------------|--------------|-----------|
| `main_.py` | `main.py` | Código principal (auto-executa no boot) |
| `lib_rs485.py` | `lib_rs485.py` | Biblioteca RS485/Modbus RTU |
| `lib_ihm.py` | `lib_ihm.py` | Biblioteca para display ST7920 |
| `config.json` | `config.json` | Configurações exportadas |

## ⚠️ Observações Importantes

### Por que main_.py?

Durante o desenvolvimento, o arquivo se chama `main_.py` para evitar que seja executado automaticamente no Pico. No upload, ele é **renomeado para `main.py`** automaticamente, garantindo que será executado no boot.

### Conexão em Busy

O problema de conexão "busy" foi resolvido! Agora:

- ✅ Sistema detecta conexão existente ao abrir o diálogo
- ✅ Botão "Desconectar" sempre disponível quando conectado
- ✅ Uma única conexão gerenciada globalmente
- ✅ Não há múltiplas tentativas de conexão simultâneas

### Modo Simulação

Se `pyserial` não estiver instalado, o sistema opera em **modo simulação**:
- Simula portas disponíveis
- Simula conexão e upload
- Útil para testar interface sem hardware

## 🎯 Fluxo Completo

```
1. Desenvolver LADDER
   ↓
2. Configurar RS485
   ↓
3. Exportar Python (Arquivo → Exportar → Python)
   ↓
4. Conectar Pico (Pico → Conectar Pico)
   ↓
5. Upload (📤 Upload)
   ↓
6. Soft Reset (opcional)
   ↓
7. Código executando no Pico!
```

## 🐛 Troubleshooting

### Pico não aparece na lista
- Verifique cabo USB (deve ser cabo de dados, não só carga)
- Verifique se MicroPython está instalado no Pico
- Pressione BOOTSEL no Pico enquanto conecta para forçar detecção

### Upload falha
- Verifique conexão serial
- Tente desconectar e reconectar
- Execute Ctrl+C no terminal REPL do Pico para liberar
- Aumente timeout nas configurações

### Conexão "busy"
- Feche outros programas que possam estar usando a porta (Thonny, etc)
- Use o botão "Desconectar" no diálogo antes de fechar
- Reinicie o Pico desconectando e reconectando USB

## 📚 Referências

- **MicroPython**: https://micropython.org/
- **Raspberry Pi Pico**: https://www.raspberrypi.com/documentation/microcontrollers/
- **Modbus RTU**: Protocolo implementado na biblioteca RS485

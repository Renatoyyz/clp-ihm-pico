# 🔍 DEBUG: Upload não funciona

## Como testar o upload

### Opção 1: Via Interface (app.py)

1. Execute a aplicação:
```bash
cd /Volumes/RenatoDados/Projetos/clp-ihm-pico/interface_ladder
python app.py
```

2. Conecte ao Pico:
   - Menu: **Pico → Conectar Pico** (Ctrl+P)
   - Selecione a porta do Pico
   - Clique em **🔌 Conectar**
   - Verifique se status mostra **🟢 Conectado**

3. Gere o código (se ainda não gerou):
   - Menu: **Arquivo → Exportar → Python**
   - Confirme que arquivos foram criados em `generated_code/`

4. Faça o upload:
   - Clique no botão **📤 Upload** na toolbar
   - Escolha "📦 Todos" ou "📄 Apenas main_.py"
   - Aguarde o upload

5. Verifique os logs na área inferior da interface

### Opção 2: Script de Teste (com debug)

Execute o script de teste que mostra logs detalhados:

```bash
cd /Volumes/RenatoDados/Projetos/clp-ihm-pico/interface_ladder
python test_upload.py
```

Este script:
- Verifica se está conectado
- Cria arquivo de teste pequeno
- Tenta fazer upload
- Mostra logs detalhados de cada etapa
- Tenta verificar arquivo no Pico
- Tenta fazer upload do main_.py

### Opção 3: Teste Manual no REPL

1. Abra o terminal REPL do Pico (no VS Code ou via screen):
```bash
screen /dev/cu.usbmodem* 115200
```

2. Pressione Ctrl+C para interromper

3. Digite manualmente:
```python
with open('test.py', 'w') as f:
    f.write('print("hello")')
print('DONE')
```

4. Pressione Enter e verifique se aparece "DONE"

5. Liste arquivos:
```python
import os
os.listdir()
```

Se isso funcionar, o problema está no código de upload da interface.

## Possíveis Problemas

### 1. Pico não está realmente conectado
**Sintoma**: Upload diz "não conectado" ou falha imediatamente  
**Solução**: 
- Verifique cabo USB (deve ser cabo de dados)
- Reconecte o Pico
- Verifique se outra aplicação está usando a porta (Thonny, etc)

### 2. MicroPython travado
**Sintoma**: Upload trava ou não responde  
**Solução**:
- Abra terminal REPL
- Pressione Ctrl+C várias vezes
- Pressione Ctrl+D para soft reset
- Tente novamente

### 3. Arquivo muito grande
**Sintoma**: Upload começa mas não termina  
**Solução**:
- O método atual funciona melhor com arquivos pequenos
- Para arquivos grandes, use `ampy` (instale: `pip install adafruit-ampy`)

### 4. Buffer serial cheio
**Sintoma**: Upload falha com timeout  
**Solução**:
- Aumentar delays no código
- Usar chunks menores (já está em 128 bytes)
- Limpar buffer antes de cada operação

## O que o script test_upload.py mostra

Quando você executar `python test_upload.py`, verá logs como:

```
[UPLOAD] Iniciando upload: /tmp/test_upload.py → test_upload.py
[UPLOAD] Arquivo lido: 123 bytes
[UPLOAD] Usando modo paste do MicroPython...
[UPLOAD] Buffer limpo
[UPLOAD] Execução interrompida
[UPLOAD] Buffer limpo: 15 bytes descartados
[UPLOAD] Comando paste enviado (Ctrl+E)
[UPLOAD] Resposta paste: b'paste mode; Ctrl-C to cancel, Ctrl-D to finish\n'
[UPLOAD] Conteúdo preparado: 123 bytes
[UPLOAD] Script criado: 156 bytes
[UPLOAD] Script enviado
[UPLOAD] Saída do modo paste (Ctrl+D)
[UPLOAD] Lido chunk 0: 45 bytes
[UPLOAD] Lido chunk 1: 12 bytes
[UPLOAD] Resposta completa: 57 bytes
[UPLOAD] ✅ Upload confirmado por marcador UPLOAD_OK
```

Se aparecer "❌ Upload falhou", os logs mostrarão exatamente onde parou.

## Próximos Passos

1. **Execute test_upload.py primeiro** para ver logs detalhados
2. **Copie os logs** e me envie se não funcionar
3. **Tente comando manual no REPL** para confirmar que Pico responde
4. **Verifique se ampy funciona**: `ampy --port /dev/cu.usbmodem* ls`

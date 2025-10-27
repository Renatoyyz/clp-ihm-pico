# Interface LADDER - CLP-IHM-PICO

## 📋 Descrição

Interface gráfica visual para programação LADDER do Raspberry Pi Pico, desenvolvida em PyQt5.

## 🚀 Funcionalidades Implementadas

### ✅ **Janela Principal Completa**
- **Menus estruturados**: Arquivo, Editar, Pico, Configurações, Ajuda
- **Interface dividida em painéis**:
  - Painel esquerdo: Biblioteca de componentes LADDER
  - Centro: Área de desenho/programação visual
  - Painel direito: Propriedades dos elementos
  - Base: Console de logs e saída
- **Barra de ferramentas** com ações principais
- **Barra de status** com indicador de conexão

### ✅ **Sistema de Configuração Pico (FUNCIONAL)**
- **Detecção automática** de portas seriais
- **Identificação inteligente** de Raspberry Pi Pico
- **Conexão real** com comunicação serial
- **Monitor em tempo real** da saída do Pico
- **Comandos de teste** pré-definidos
- **Console interativo** para comandos personalizados
- **Auto-conexão** quando Pico é detectado

## 🗂️ Estrutura de Arquivos

```
interface_ladder/
├── app.py              # Aplicação principal (entry point)
├── main_window.py      # Janela principal da interface
├── config_dialog.py    # Diálogo de configuração do Pico (FUNCIONAL)
└── README.md          # Este arquivo
```

## 🎯 Como Executar

### Prerequisitos
- Python 3.10+
- PyQt5 (instalado no ambiente virtual)
- pyserial (para comunicação com Pico)

### Execução
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar aplicação
cd interface_ladder
python3 app.py
```

## 🔧 Funcionalidades por Menu

### 📁 **Menu Arquivo**
- ✅ Estrutura criada
- 🔲 Novo projeto (placeholder)
- 🔲 Abrir projeto (placeholder)
- 🔲 Salvar projeto (placeholder)
- 🔲 Exportar para Python (placeholder)
- 🔲 Exportar como imagem (placeholder)

### ✏️ **Menu Editar**
- ✅ Estrutura criada
- 🔲 Desfazer/Refazer (placeholder)
- 🔲 Copiar/Colar (placeholder)

### 🥧 **Menu Pico**
- ✅ Estrutura criada
- 🔲 Upload para Pico (placeholder)
- 🔲 Executar no Pico (placeholder)
- 🔲 Reset Pico (placeholder)

### ⚙️ **Menu Configurações**
- ✅ **Conexão Pico** - **TOTALMENTE FUNCIONAL** 🎉
  - Detecção automática de portas
  - Conexão real com Pico
  - Monitor de saída
  - Comandos de teste
  - Console interativo
- 🔲 Preferências gerais (placeholder)

### ❓ **Menu Ajuda**
- ✅ Sobre (funcional)
- 🔲 Manual do usuário (placeholder)

## 🖥️ Interface Detalhada

### **Janela Principal**
- **Layout responsivo** com splitters redimensionáveis
- **Painéis organizados** para workflow otimizado
- **Console integrado** com syntax highlighting
- **Status bar** com informações de conexão

### **Diálogo de Configuração Pico**
#### **Aba Conexão**
- Lista de portas com atualização automática
- Identificação visual de Raspberry Pi Pico (🥧)
- Configuração de baudrate e timeout
- Status visual da conexão (🔴/🟡/🟢)

#### **Aba Monitor**
- Saída em tempo real do Pico
- Console estilo terminal com cores
- Auto-scroll configurável
- Salvar logs em arquivo

#### **Aba Testes**
- **8 comandos pré-definidos**:
  - LED ON/OFF
  - Leitura de temperatura
  - Informações do sistema
  - Teste de memória
  - Listagem de arquivos
  - Reset soft
  - Teste de GPIO
- **Console personalizado** para comandos livres

## 🎨 Design e Estilo

- **Interface moderna** com cores suaves
- **Ícones emoji** para fácil identificação
- **Feedback visual** com cores de status
- **Layout profissional** similar a IDEs industriais

## 🔄 Próximos Passos

1. **Implementar editor visual LADDER**
2. **Sistema de arrastar e soltar** para componentes
3. **Compilador LADDER → Python**
4. **Sistema de projetos** com salvamento
5. **Biblioteca de componentes** expansível
6. **Simulador integrado**

## 📊 Status do Projeto

- **Base da Interface**: ✅ 100% Completa
- **Sistema de Conexão**: ✅ 100% Funcional
- **Menus e Navegação**: ✅ 100% Estruturados
- **Editor LADDER Visual**: 🔲 Próxima fase
- **Compilador**: 🔲 Fase futura

---

**🚀 Pronto para desenvolvimento da programação visual LADDER!**
# 🔄 NOVO FLUXO IHM - Atualização v2.0

## 📋 **Mudanças Implementadas**

### ✅ **1. Novo Sistema de Adição de Componentes**
- **❌ Antes:** Arrastar componentes IHM diretamente para o canvas
- **✅ Agora:** Botões "+" para adicionar componentes no editor IHM

### ✅ **2. Menu de Contexto no Display LADDER**
- **❌ Antes:** Clique simples para abrir configuração
- **✅ Agora:** Clique direito → "Configurar IHM" para abrir editor

### ✅ **3. Componentes Fixam Corretamente**
- **❌ Antes:** Componentes não persistiam visualmente
- **✅ Agora:** Componentes aparecem imediatamente e persistem

---

## 🎯 **Novo Fluxo de Trabalho**

### **Passo 1: Adicionar Display ao LADDER**
1. Execute `python main.py`
2. Na **Biblioteca de Componentes LADDER**
3. Localize o grupo **"IHM"**
4. **Arraste** o componente **"Display IHM"** para o **Editor LADDER**

### **Passo 2: Configurar IHM (Clique Direito)**
1. No **Editor LADDER**, localize o bloco **Display IHM**
2. **Clique direito** no bloco Display
3. Selecione **"🖥️ Configurar IHM"** no menu de contexto
4. Janela do **Editor IHM** será aberta

### **Passo 3: Adicionar Componentes (Botões +)**
1. No **Editor IHM**, painel esquerdo tem categorias de componentes
2. **Clique nos botões** `+ Nome do Componente` para adicionar
3. Componentes aparecem **automaticamente** no canvas 128x64
4. Posicionamento inicial é **centro da tela** com offset para não sobrepor

### **Passo 4: Configurar Propriedades**
1. **Clique** em qualquer componente no canvas
2. Painel direito mostra **propriedades** do componente selecionado
3. Configure **texto, variáveis, ações, etc.**
4. Mudanças são aplicadas **em tempo real**

### **Passo 5: Gerenciar Telas**
1. Use **"+ Nova Tela"** no gerenciador de telas
2. **Troque entre telas** para criar múltiplas interfaces
3. Cada tela mantém seus **componentes independentemente**

### **Passo 6: Salvar Configuração**
1. Use **"💾 Salvar Config"** para persistir todas as telas
2. **Carregamento automático** na próxima sessão
3. Use **"📁 Carregar Config"** para restaurar backup

---

## 🖱️ **Controles da Interface**

### **Canvas IHM (Centro):**
- **Visualização:** Área 128x64 pixels (escala 4x para melhor visibilidade)
- **Seleção:** Clique em componentes para selecionar
- **Propriedades:** Componente selecionado aparece no painel direito
- **Grid:** Linhas auxiliares a cada 8 pixels

### **Biblioteca de Componentes (Esquerda):**
- **📝 Textos e Campos:** `+ Texto Estático`, `+ Campo Entrada`, etc.
- **🔘 Botões e Controles:** `+ Botão`, `+ Botão Liga/Desliga`, etc.
- **📊 Gráficos:** `+ Gráfico Barras`, `+ Indicador Circular`, etc.
- **✏️ Entrada de Dados:** `+ Campo Numérico`, `+ Seletor`, etc.
- **🖼️ Elementos Visuais:** `+ Ícone/Símbolo`, `+ Linha`, etc.

### **Gerenciador de Telas (Esquerda Superior):**
- **Lista de Telas:** Clique para trocar entre telas
- **+ Nova Tela:** Criar tela adicional
- **🗑️ Excluir:** Remover tela selecionada
- **⚙️ Propriedades:** Configurar timeout, navegação, etc.

### **Painel de Propriedades (Direita):**
- **Posição:** X, Y (coordenadas)
- **Tamanho:** Largura, Altura
- **Conteúdo:** Texto, variável, formato
- **Comportamento:** Ação, estado, validação

---

## 🔧 **Componentes Disponíveis**

### 📝 **Textos e Campos**
- **Texto Estático:** Labels fixos e títulos
- **Campo Entrada:** Input de dados do usuário  
- **Label Variável:** Valores dinâmicos de variáveis
- **Status Texto:** Textos condicionais baseados em estado

### 🔘 **Botões e Controles**
- **Botão:** Ações configuráveis (próxima tela, função)
- **Botão Liga/Desliga:** Toggle de estados
- **Seletor:** Lista de opções para escolha
- **Indicador LED:** Status visual ligado/desligado

### 📊 **Gráficos**
- **Gráfico Barras:** Barras horizontais de valores
- **Gráfico XY:** Linhas temporais e tendências
- **Barra Progresso:** Progressão percentual
- **Indicador Circular:** Medidores tipo velocímetro

### ✏️ **Entrada de Dados**
- **Campo Numérico:** Entrada de números
- **Botões Numéricos:** Teclado virtual
- **Campo Texto:** Entrada de strings

### 🖼️ **Elementos Visuais**
- **Ícone/Símbolo:** Gráficos decorativos
- **Linha:** Elementos de separação
- **Retângulo:** Molduras e containers
- **Moldura:** Agrupamento visual

---

## 💡 **Dicas de Uso**

### **✅ Melhores Práticas:**
- **Planeje** quantas telas precisará antes de começar
- **Use nomes** descritivos para componentes e telas
- **Teste** a navegação entre telas
- **Salve** frequentemente com "Salvar Config"
- **Configure timeout** para navegação automática

### **⚠️ Limitações Técnicas:**
- **Resolução:** 128x64 pixels (tamanho físico do display)
- **Cores:** Monocromático (preto sobre fundo verde)
- **Fontes:** Limitadas pelo hardware ST7920
- **Performance:** Evite muitos componentes por tela

### **🔍 Solução de Problemas:**
- **Componentes não aparecem:** Verifique se estão dentro da área 128x64
- **Propriedades não salvam:** Certifique-se de pressionar Enter após editar
- **Tela não carrega:** Use "Carregar Config" ou restart da aplicação
- **Performance lenta:** Reduza número de componentes complexos

---

## 🎉 **Sistema Completamente Funcional!**

### **✅ Funcionalidades Entregues:**
- ✅ **Drag & Drop:** Apenas Display IHM → Editor LADDER
- ✅ **Menu de Contexto:** Clique direito → Configurar IHM
- ✅ **Adição por Botões:** Interface intuitiva com botões "+"
- ✅ **Fixação Garantida:** Componentes permanecem no canvas
- ✅ **Persistência:** Salvamento/carregamento automático
- ✅ **Multi-telas:** Sistema completo de gerenciamento
- ✅ **Propriedades:** Configuração individual de cada componente

### **🚀 Para Usar Agora:**
```bash
python main.py
```

**Fluxo:** Arrastar Display → LADDER → Clique Direito → Configurar → Adicionar com botões "+" → Configurar propriedades → Salvar! 🎯
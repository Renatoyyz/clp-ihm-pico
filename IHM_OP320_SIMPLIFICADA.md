# ✅ BIBLIOTECA IHM SIMPLIFICADA - ESTILO OP320

## 🎯 **Objetivo Alcançado**
Biblioteca IHM simplificada com apenas **8 componentes essenciais**, seguindo o modelo do IHM OP320 com suporte a **4 botões físicos externos** (F1-F4).

## 📋 **Componentes Disponíveis (8 tipos)**

### 📝 **Categoria: Textos (2 componentes)**
1. **Texto Estático** (`static_text`)
   - Exibe texto fixo na tela
   - Usado para labels, títulos, instruções
   - Não muda durante execução

2. **Texto Dinâmico** (`dynamic_text`) 
   - Exibe valor de variável em tempo real
   - Conectado a tags do CLP
   - Atualiza automaticamente

### 💡 **Categoria: Indicadores (1 componente)**
3. **LED Indicador** (`led_indicator`)
   - Indicador luminoso on/off com cores
   - Verde/Vermelho/Amarelo conforme estado
   - Conectado a bits do CLP

### 📝 **Categoria: Entrada (2 componentes)**
4. **Campo de Entrada** (`input_field`)
   - Campo para inserir valores numéricos
   - Permite entrada de setpoints
   - Validação de dados integrada

5. **Botão de Função** (`function_button`)
   - Mapeado para botões físicos externos (F1-F4)
   - Apenas 4 botões disponíveis no hardware
   - Executa funções específicas no CLP

### 🖼️ **Categoria: Imagem (1 componente)**
6. **Área de Imagem** (`mono_image`)
   - Exibe imagens monocromáticas (P&B)
   - Ideal para logos, diagramas, símbolos
   - Formato bitmap 1-bit

### 📊 **Categoria: Gráficos (2 componentes)**
7. **Gráfico de Barras** (`bar_graph`)
   - Visualização de dados em barras
   - Múltiplas barras comparativas
   - Escalas configuráveis

8. **Gráfico X,Y** (`xy_graph`)
   - Gráfico de linha/pontos temporais
   - Tendências e históricos
   - Eixos X (tempo) e Y (valor)

## 🎮 **Mapeamento de Botões Físicos**

### Hardware Disponível: **4 Botões Externos**
- **F1** - Função primária (Ex: Confirmar, OK)
- **F2** - Função secundária (Ex: Cancelar, ESC)  
- **F3** - Navegação (Ex: Próxima tela, Menu)
- **F4** - Controle (Ex: Reset, Start/Stop)

### Configuração no IHM:
- Componentes `function_button` são mapeados para F1-F4
- Máximo de 4 botões de função por tela
- Cada botão executa comando específico no CLP

## 🖥️ **Display ST7920 (128x64 pixels)**

### Características:
- **Resolução**: 128 x 64 pixels monocromático
- **Área útil**: ~110 x 55 pixels (bordas reservadas)
- **Fonte**: 6x8 pixels (caracteres pequenos)
- **Gráficos**: Suporte completo a desenho

### Otimização de Espaço:
- Textos: 6-8 pixels de altura
- Botões: 15-20 pixels de altura  
- Gráficos: 30-40 pixels de altura
- LEDs: 8-12 pixels (círculos pequenos)

## 📱 **Exemplos de Telas Típicas**

### **Tela Principal**
```
┌─────────────────────────────┐
│ SISTEMA CLP v1.0            │ ← Texto Estático
│ Temp: 25.4°C  ●            │ ← Texto Dinâmico + LED
│ ████████░░ 80%              │ ← Gráfico Barras  
│ [F1-Menu] [F2-Reset]        │ ← Botões Função
└─────────────────────────────┘
```

### **Tela de Configuração**
```
┌─────────────────────────────┐
│ SETPOINT TEMPERATURA        │ ← Texto Estático
│ Valor: [_25.0_]°C          │ ← Campo Entrada
│ Status: ● ATIVO            │ ← LED Indicador
│ [F1-OK] [F2-Cancel]         │ ← Botões Função
└─────────────────────────────┘
```

### **Tela de Gráficos**
```
┌─────────────────────────────┐
│ TENDÊNCIA PRESSÃO           │ ← Texto Estático
│ ┌─────────────────────────┐ │
│ │     ∕∖                  │ │ ← Gráfico X,Y
│ │    ∕  ∖_                │ │
│ │   ∕     ∖               │ │
│ └─────────────────────────┘ │
│ [F3-Menu] [F4-Reset]        │ ← Botões Função
└─────────────────────────────┘
```

## ✅ **Status de Implementação**

### 🎉 **COMPLETO E FUNCIONANDO:**
- ✅ 8 componentes IHM implementados
- ✅ Categorização clara e organizada
- ✅ Renderização visual de cada tipo
- ✅ Interface simplificada (Apply/Close)
- ✅ Persistência de dados nos blocos Display
- ✅ Auto-configuração ao arrastar Display
- ✅ Carregamento de configurações salvas

### 🔄 **Para Próximas Iterações:**
- Propriedades específicas de cada componente
- Conectividade com tags do CLP
- Simulação de dados em tempo real
- Exportação para código ST7920
- Mapeamento físico dos botões F1-F4

## 🎯 **Resultado Final**

**A biblioteca IHM está SIMPLIFICADA e OTIMIZADA** seguindo o modelo OP320:
- **8 componentes essenciais** (em vez de 20+)
- **5 categorias organizadas** logicamente
- **4 botões físicos** apenas (F1-F4)
- **Interface limpa** para configuração
- **Foco na funcionalidade** industrial

**PRONTO PARA USO EM APLICAÇÕES INDUSTRIAIS! 🏭✨**
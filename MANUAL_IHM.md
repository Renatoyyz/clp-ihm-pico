# Sistema IHM - Interface Homem-Máquina
**Display ST7920 128x64 para Raspberry Pi Pico**

## 🎯 Funcionalidades Implementadas

### ✅ Sistema Completo de IHM
- **Canvas de Design:** Área visual 128x64 pixels para criação de interfaces
- **Biblioteca de Componentes:** 20+ componentes organizados em categorias
- **Gerenciador de Telas:** Sistema para criar e navegar entre múltiplas telas
- **Propriedades:** Painel para configurar cada componente individualmente
- **Persistência:** Salvamento automático e manual das configurações

### 📱 Componentes Disponíveis

#### 🖥️ Display
- **Texto Estático:** Labels e títulos fixos
- **Texto Dinâmico:** Valores de variáveis em tempo real
- **Indicador LED:** Status visual ligado/desligado

#### 🎛️ Controles
- **Botões:** Ações configuráveis (próxima tela, função personalizada)
- **Seletor:** Lista de opções para escolha

#### 📊 Gráficos
- **Barra de Progresso:** Visualização percentual
- **Gauge (Velocímetro):** Medidores circulares
- **Gráfico de Linha:** Tendências temporais
- **Gráfico de Barras:** Comparações de valores

#### ✏️ Entrada
- **Campo de Texto:** Entrada de dados do usuário
- **Botões Numéricos:** Teclado virtual para valores

## 🚀 Como Usar

### 1. **Executar a Aplicação**
```bash
python main.py
```

### 2. **Acessar Configuração IHM**
- Na biblioteca de componentes LADDER, localize o grupo **"IHM"**
- Clique no componente **"Display IHM"** para abrir a configuração
- Alternativamente, arraste o componente para o canvas LADDER

### 3. **Criar Telas**
- No **Gerenciador de Telas** (painel esquerdo):
  - Clique **"+ Nova Tela"** para criar
  - Digite nome da tela
  - Configure propriedades (timeout, navegação, etc.)

### 4. **Adicionar Componentes**
- No **Canvas Central** (128x64 pixels):
  - Arraste componentes da biblioteca para a área de design
  - Posicione conforme necessário
  - Componentes são salvos automaticamente

### 5. **Configurar Propriedades**
- No **Painel de Propriedades** (direita):
  - Clique em qualquer componente no canvas
  - Configure texto, variáveis, ações, etc.
  - Mudanças são aplicadas em tempo real

### 6. **Salvar/Carregar Configurações**
- **💾 Salvar Config:** Salva todas as telas em `ihm_config.json`
- **📁 Carregar Config:** Restaura configuração salva
- **Carregamento Automático:** Configuração é carregada automaticamente na inicialização

### 7. **Aplicar ao Projeto**
- Clique **"✅ Aplicar"** para finalizar
- As telas configuradas ficam disponíveis para o Raspberry Pi Pico

## 💾 Sistema de Persistência

### Arquivo de Configuração: `ihm_config.json`
```json
{
  "version": "1.0",
  "screens": [
    {
      "name": "Tela Principal",
      "id": 1,
      "properties": {
        "background_color": "light_green",
        "timeout": 0,
        "show_header": true
      },
      "components": [
        {
          "type": "text",
          "name": "Título",
          "x": 10,
          "y": 5,
          "width": 60,
          "height": 12,
          "properties": {
            "text": "Sistema IHM",
            "font_size": 8
          }
        }
      ]
    }
  ]
}
```

### Funcionalidades de Persistência:
- ✅ **Salvamento Automático:** Componentes são salvos ao serem adicionados/movidos
- ✅ **Salvamento Manual:** Botão "Salvar Config" para backup
- ✅ **Carregamento Automático:** Configuração restaurada na inicialização
- ✅ **Carregamento Manual:** Botão "Carregar Config" para restaurar

## 🎨 Personalização de Componentes

### Propriedades Comuns:
- **Posição:** X, Y (coordenadas em pixels)
- **Tamanho:** Largura, Altura
- **Texto:** Conteúdo exibido
- **Variável:** Nome da variável para dados dinâmicos

### Propriedades Específicas:
- **Botões:** Ação (próxima tela, função)
- **Indicadores:** Estado (ligado/desligado)
- **Gráficos:** Valor mín/máx, formato
- **Entradas:** Validação, tipo de dados

## 🔧 Integração com Hardware

### Display ST7920 (128x64):
- **Resolução:** 128 pixels largura × 64 pixels altura
- **Tipo:** Monocromático (preto/verde)
- **Interface:** SPI com Raspberry Pi Pico
- **Renderização:** Pixel-perfect para o hardware

### Variáveis do Sistema:
- Componentes podem referenciar variáveis do programa LADDER
- Atualização em tempo real dos valores
- Sincronização automática com o Raspberry Pi Pico

## 🎯 Fluxo de Trabalho Completo

1. **Planejamento:** Defina quantas telas e que informações mostrar
2. **Design:** Use o canvas visual para criar cada tela
3. **Configuração:** Ajuste propriedades e navegação entre telas
4. **Teste:** Visualize no canvas como ficará no display
5. **Salvamento:** Use "Salvar Config" para backup das configurações
6. **Deploy:** Apply no projeto LADDER para enviar ao Pico

## 📊 Recursos Avançados

### Sistema Multi-Tela:
- Navegação automática (timeout)
- Navegação por botões
- Hierarquia de telas
- Tela inicial configurável

### Componentes Dinâmicos:
- Valores atualizados em tempo real
- Estados baseados em variáveis
- Formatação personalizada de números
- Textos condicionais

### Otimização para Hardware:
- Renderização otimizada para SPI
- Gestão eficiente de memória
- Atualização parcial da tela
- Economia de energia

---

## 🚀 **Sistema IHM Totalmente Funcional!**

**Funcionalidades Implementadas:**
- ✅ Canvas visual 128x64 pixels
- ✅ 20+ componentes organizados
- ✅ Gerenciador de múltiplas telas  
- ✅ Propriedades configuráveis
- ✅ Persistência automática e manual
- ✅ Integração com LADDER
- ✅ Interface completa e intuitiva

**Para começar a usar:**
```bash
python main.py
```
**→ Biblioteca de Componentes → IHM → Display IHM** 🎉
# XML Translator - Estrutura Profissional

Tradutor automatizado de arquivos XML de localização do inglês para português (pt-BR) com **overrides baseados em texto** e **arquitetura modular**.

## Estrutura do Projeto

```
xml-translator/
├── src/
│   └── xml_translator/
│       ├── core/                 # Módulos principais
│       │   ├── auto_translator.py    # Google Translate + Overrides
│       │   └── translator.py         # Processamento XML
│       └── utils/                # Utilitários
│           └── logger.py             # Sistema de logging
├── config/                       # Configurações
│   ├── overrides.json               # Overrides ativos
│   └── overrides.example.json       # Exemplo de overrides
├── examples/                     # Arquivos de exemplo
├── logs/                        # Logs do sistema
├── tests/                       # Testes automatizados
├── docs/                        # Documentação
│   └── OVERRIDES.md                # Guia de overrides
├── main.py                      # Script principal
└── pyproject.toml              # Configuração Poetry
```

## Características

- **Overrides baseados em texto** - Substitui palavras/frases específicas no XML  
- **Reutilização inteligente** - Uma entrada override resolve múltiplas chaves XML  
- **Tradução automática** - Google Translate para texto não mapeado  
- **Sistema de prioridades** - Override → Google → Original  
- **Arquitetura modular** - Separação clara de responsabilidades  
- **Logging estruturado** - Logs detalhados em arquivos diários  

## Instalação e Uso

```bash
# Instalar dependências
poetry install

# Executar tradutor
poetry run xml-translator
```

## Sistema de Overrides - NOVIDADE

### Como Funciona
O sistema substitui **texto específico** encontrado no XML, independente da chave onde aparece.y

**Override:**
```json
{
  "Settings": "Definições"
}
```

**Resultado:** Todas as 3 chaves ficam com "Definições"

## Como Adicionar Overrides

1. **Identifique o texto** no XML original (ex: "Dashboard")
2. **Adicione no arquivo** `config/overrides.json`:
   ```json
   {
     "Dashboard": "Painel de Controle"
   }
   ```
3. **Execute novamente** o tradutor

**Documentação completa**: [`docs/OVERRIDES.md`](docs/OVERRIDES.md)

## Uso Básico

```bash
poetry run xml-translator
```

**Fluxo automático:**
1. Detecta arquivos XML no diretório
2. Permite escolha do arquivo 
3. Processa traduções (Override → Google → Original)
4. Gera arquivo `*_pt-BR.xml`

### Estrutura XML Suportada
```xml
<?xml version="1.0" encoding="utf-8"?>
<localization culture="en-US">
  <group name="Common">
    <string key="Title">Dashboard</string>
    <string key="Cancel">Cancel</string>
  </group>
</localization>
```

## Desenvolvimento

### Executar Testes
```bash
poetry run pytest tests/
```

## Funcionalidades

### Implementadas
- **Overrides baseados em texto** - Sistema inteligente de substituição
- **Tradução automática** - Google Translate integrado
- **Logging estruturado** - Logs detalhados em arquivos diários
- **Arquitetura modular** - Código organizado e manutenível

### Fluxo de Processamento
1. **Inicialização** → Setup logging + tradutor
2. **Detecção** → Buscar arquivos XML disponíveis  
3. **Carregamento** → Parser XML com validação
4. **Extração** → Identificar strings traduzíveis
5. **Tradução** → **Override** → **Google** → **Original**
6. **Aplicação** → Atualizar XML com traduções
7. **Salvamento** → Gerar arquivo pt-BR  
8. **Relatório** → Estatísticas e logs

